from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

from bigeye_sdk.generated.com.bigeye.models.generated import (
    CustomRepositorySyncRequest,
    CustomRepositorySyncNode,
    CustomRepositorySyncEdge,
    CustomRepositorySyncNodeLookup,
    CatalogAttribute,
    RelationshipType,
    DataNodeType,
    IntegrationType,
    CustomNodeType as CustomNodeTypeProto,
    CustomIntegrationType as CustomIntegrationTypeProto
)
from bigeye_sdk.log import get_logger

log = get_logger(__name__)


@dataclass
class CatalogDeploymentResult:
    """
    Result of deploying catalog infrastructure (integration type, node types, repository).

    Attributes:
        integration_type_id: ID of the integration type
        repository_id: ID of the repository
        node_type_ids: Dictionary mapping node type names to their IDs
        created: True if new resources were created
        updated: True if existing resources were updated
    """
    integration_type_id: int
    repository_id: int
    node_type_ids: Dict[str, int] = field(default_factory=dict)
    created: bool = False
    updated: bool = False


class SimpleIntegrationType(str, enum.Enum):
    """
    Simple facade for IntegrationType enum (Pydantic v2).
    Maps user-friendly names to protobuf IntegrationType values.
    """
    UNSPECIFIED = "INTEGRATION_TYPE_UNSPECIFIED"
    BI_TOOL = "INTEGRATION_TYPE_BI_TOOL"
    ETL_TOOL = "INTEGRATION_TYPE_ETL_TOOL"
    DATABASE = "INTEGRATION_TYPE_DATABASE"

    def to_protobuf(self) -> IntegrationType:
        """Convert to protobuf IntegrationType"""
        return IntegrationType[self.value]


class SimpleCustomNodeType(BaseModel):
    """
    Represents a custom node type definition (Pydantic v2).

    Attributes:
        name: Singular display name (e.g., "Schema", "Table")
        name_plural: Plural display name (e.g., "Schemas", "Tables")
        allowed_parent_types: List of node type names that can be parents
        id: Optional ID if this node type already exists
    """
    name: str
    name_plural: str
    allowed_parent_types: Optional[List[str]] = None
    id: Optional[int] = None
    is_column_display: Optional[bool] = False

    def to_protobuf(self, integration_type_id: int) -> CustomNodeTypeProto:
        """Convert to protobuf CustomNodeType."""
        parent_types = []
        if self.allowed_parent_types:
            parent_types = [
                CustomNodeTypeProto(name=parent_name)
                for parent_name in self.allowed_parent_types
            ]

        return CustomNodeTypeProto(
            id=self.id or 0,
            name=self.name,
            name_plural=self.name_plural,
            integration_type=CustomIntegrationTypeProto(id=integration_type_id),
            allowed_parent_types=parent_types,
            is_column_display=self.is_column_display
        )


class NodeTypeResolution(str, enum.Enum):
    """
    Strategy for resolving node type references in the configuration file.

    - BY_NAME: Resolve node type names to IDs by looking them up via API
    - BY_ID: Use node type IDs directly (no name resolution)
    - MIXED: Allow both - prefer ID if present, otherwise resolve name
    """
    BY_NAME = "BY_NAME"
    BY_ID = "BY_ID"
    MIXED = "MIXED"


class SimpleNodeLookup(BaseModel):
    """
    Reference to a node outside the current repository.

    Used in edges to reference nodes that exist in the catalog but are not
    part of this repository (e.g., warehouse tables, BI entities).

    Note: As of the current implementation, only `node_id` is fully supported.
    Other fields are reserved for future use.

    Attributes:
        node_id: Direct node ID reference (fully supported)
        table_id: Table ID for passthrough column lookup (used with passthrough_external_id)
        node_name: Node name for lookup (future)
        node_container_name: Container name for scoped lookup (future)
        source_id: Source/warehouse ID for lookup (future)
        source_node_type: Source node type for lookup (future)
    """
    node_id: Optional[int] = None
    table_id: Optional[int] = None
    node_name: Optional[str] = None
    node_container_name: Optional[str] = None
    source_id: Optional[int] = None
    source_node_type: Optional[str] = None

    @model_validator(mode='after')
    def validate_lookup(self):
        """Validate that at least one lookup field is provided."""
        if not any([
            self.node_id,
            self.node_name,
            self.source_id,
            self.table_id
        ]):
            raise ValueError("At least one lookup field must be provided (node_id, node_name, source_id, or table_id)")
        return self

    def to_protobuf(self) -> CustomRepositorySyncNodeLookup:
        """Convert to protobuf CustomRepositorySyncNodeLookup."""
        return CustomRepositorySyncNodeLookup(
            node_id=self.node_id or 0,
            node_name=self.node_name or "",
            node_container_name=self.node_container_name or "",
            source_id=self.source_id or 0,
            source_node_type=DataNodeType[self.source_node_type] if self.source_node_type else DataNodeType.DATA_NODE_TYPE_UNSPECIFIED
        )


class SimpleRepositorySyncNode(BaseModel):
    """
    Definition of a node to sync in the repository.

    Attributes:
        external_id: Unique identifier for this node within the repository (required)
        node_name: Display name for the node (required)
        node_type: Name of the node type (e.g., "DAG", "Task") - used with BY_NAME resolution
        node_type_id: Direct ID of the node type - used with BY_ID resolution
        container_external_id: External ID of the parent/container node (creates hierarchy)
        attributes: Key-value pairs for catalog attributes (metadata)
        is_attributes_empty: If true, clears all repository-managed attributes
    """
    external_id: str
    node_name: str
    node_type: Optional[str] = None
    node_type_id: Optional[int] = None
    container_external_id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    is_attributes_empty: bool = False

    @model_validator(mode='after')
    def validate_node_type(self):
        """Validate that either node_type or node_type_id is provided."""
        if not self.node_type and not self.node_type_id:
            raise ValueError(
                f"Node '{self.external_id}': either node_type or node_type_id must be provided"
            )
        return self

    def to_protobuf(self, node_type_id: int) -> CustomRepositorySyncNode:
        """Convert to protobuf CustomRepositorySyncNode."""
        attributes = []
        if self.attributes:
            attributes = [
                CatalogAttribute(key=k, value=v)
                for k, v in self.attributes.items()
            ]

        return CustomRepositorySyncNode(
            external_id=self.external_id,
            node_name=self.node_name,
            custom_node_type_id=node_type_id,
            container_external_id=self.container_external_id or "",
            attributes=attributes,
            is_attributes_empty=self.is_attributes_empty
        )


class SimpleRepositorySyncEdge(BaseModel):
    """
    Definition of a lineage edge between two nodes.

    Attributes:
        upstream_external_id: External ID of upstream node (for nodes in this repository)
        upstream_node: Lookup for upstream node (for external nodes)
        downstream_external_id: External ID of downstream node (for nodes in this repository)
        downstream_node: Lookup for downstream node (for external nodes)
        relationship_type: Always "LINEAGE" for user-submitted edges
        expand_upstream: If true, automatically expand upstream table to column-level nodes
        expand_downstream: If true, automatically expand downstream table to column-level nodes
        passthrough_external_id: If set, creates column mappings through this intermediate node
            (e.g., table -> activity -> table). Requires upstream_node and downstream_node with node_ids.
    """
    upstream_external_id: Optional[str] = None
    upstream_node: Optional[SimpleNodeLookup] = None
    downstream_external_id: Optional[str] = None
    downstream_node: Optional[SimpleNodeLookup] = None
    relationship_type: str = "LINEAGE"
    expand_upstream: bool = False
    expand_downstream: bool = False
    passthrough_external_id: Optional[str] = None

    @model_validator(mode='after')
    def validate_edge(self):
        """Validate that edge has exactly one upstream and one downstream reference."""
        # Validate upstream
        has_upstream_id = bool(self.upstream_external_id)
        has_upstream_node = bool(self.upstream_node)

        if not (has_upstream_id or has_upstream_node):
            raise ValueError("Either upstream_external_id or upstream_node must be provided")
        if has_upstream_id and has_upstream_node:
            raise ValueError("Only one of upstream_external_id or upstream_node should be provided")

        # Validate downstream
        has_downstream_id = bool(self.downstream_external_id)
        has_downstream_node = bool(self.downstream_node)

        if not (has_downstream_id or has_downstream_node):
            raise ValueError("Either downstream_external_id or downstream_node must be provided")
        if has_downstream_id and has_downstream_node:
            raise ValueError("Only one of downstream_external_id or downstream_node should be provided")

        return self

    def to_protobuf(self) -> CustomRepositorySyncEdge:
        """Convert to protobuf CustomRepositorySyncEdge."""
        edge = CustomRepositorySyncEdge(
            relationship_type=RelationshipType.RELATIONSHIP_TYPE_LINEAGE
        )

        if self.upstream_external_id:
            edge.upstream_external_id = self.upstream_external_id
        elif self.upstream_node:
            edge.upstream_node = self.upstream_node.to_protobuf()

        if self.downstream_external_id:
            edge.downstream_external_id = self.downstream_external_id
        elif self.downstream_node:
            edge.downstream_node = self.downstream_node.to_protobuf()

        return edge


class SimpleRepositoryDefinition(BaseModel):
    """Complete repository definition including integration type and node types."""
    name: str
    id: Optional[int] = None
    integration_name: str
    integration_type: SimpleIntegrationType = SimpleIntegrationType.ETL_TOOL
    integration_description: Optional[str] = None
    integration_icon_url: Optional[str] = None
    node_types: List[SimpleCustomNodeType] = Field(default_factory=list)

    @field_validator('integration_type', mode='before')
    @classmethod
    def convert_integration_type(cls, v):
        """
        Convert user-friendly integration type strings to enum.
        Accepts:
        - Enum member names: "ETL_TOOL", "BI_TOOL", "DATABASE"
        - Full enum values: "INTEGRATION_TYPE_ETL_TOOL", "INTEGRATION_TYPE_BI_TOOL", etc.
        - Enum objects: SimpleIntegrationType.ETL_TOOL
        """
        if isinstance(v, SimpleIntegrationType):
            return v

        if isinstance(v, str):
            # Try to match by enum member name first (e.g., "ETL_TOOL")
            try:
                return SimpleIntegrationType[v.upper()]
            except KeyError:
                pass

            # Try to match by enum value (e.g., "INTEGRATION_TYPE_ETL_TOOL")
            for member in SimpleIntegrationType:
                if member.value == v:
                    return member

            # If no match, provide helpful error message
            valid_names = ", ".join([m.name for m in SimpleIntegrationType])
            raise ValueError(
                f"Invalid integration_type '{v}'. "
                f"Valid values: {valid_names}"
            )

        return v

    @model_validator(mode='after')
    def validate_node_types(self):
        """Validate that node types are defined and parent references are valid"""
        if not self.node_types:
            raise ValueError("At least one node type must be defined")

        # Verify parent type references are valid
        node_type_names = {nt.name for nt in self.node_types}
        for node_type in self.node_types:
            if node_type.allowed_parent_types:
                for parent_name in node_type.allowed_parent_types:
                    if parent_name not in node_type_names:
                        raise ValueError(
                            f"Node type '{node_type.name}' references unknown parent type '{parent_name}'. "
                            f"Available types: {', '.join(node_type_names)}"
                        )

        return self


class CustomRepositoryConfigurationFile(BaseModel):
    """
    Configuration file for syncing custom repository lineage.
    """
    type: str = "CUSTOM_REPOSITORY_CONFIGURATION_FILE"
    repository: SimpleRepositoryDefinition
    node_type_resolution: NodeTypeResolution = NodeTypeResolution.BY_NAME
    cleanup_stale: bool = True
    nodes: List[SimpleRepositorySyncNode] = Field(default_factory=list)
    edges: List[SimpleRepositorySyncEdge] = Field(default_factory=list)

    @model_validator(mode='after')
    def validate_config(self):
        """
        Validate the configuration.

        Checks:
        - Container references exist in nodes
        - Edge external_id references exist in nodes
        """
        external_ids = {node.external_id for node in self.nodes}

        # Validate container references
        for node in self.nodes:
            if node.container_external_id and node.container_external_id not in external_ids:
                raise ValueError(
                    f"Node '{node.external_id}' references container '{node.container_external_id}' "
                    f"which is not defined in this file"
                )

        # Validate edge references (only for external_id references, not node lookups)
        for i, edge in enumerate(self.edges):
            if edge.upstream_external_id and edge.upstream_external_id not in external_ids:
                raise ValueError(
                    f"Edge #{i+1} references unknown upstream node '{edge.upstream_external_id}'"
                )
            if edge.downstream_external_id and edge.downstream_external_id not in external_ids:
                raise ValueError(
                    f"Edge #{i+1} references unknown downstream node '{edge.downstream_external_id}'"
                )

        return self

    @classmethod
    def load(cls, file_path: str) -> "CustomRepositoryConfigurationFile":
        """Load configuration from a YAML file."""
        log.info(f"Loading configuration from {file_path}")
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def save(self, file_path: str) -> None:
        """Save configuration to a YAML file."""
        log.info(f"Saving configuration to {file_path}")
        with open(file_path, 'w') as f:
            # Convert to dict, using mode='json' to serialize enums properly
            data = self.model_dump(mode='json', exclude_none=True, exclude_defaults=True)
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

    def __str__(self) -> str:
        """Return YAML representation of the configuration."""
        data = self.model_dump(mode='json', exclude_none=True, exclude_defaults=False)
        return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

    @staticmethod
    def resolve_node_type(node_type_ids: Dict[str, int], name: str) -> int:
        """Resolve node type name to ID."""
        node_type_id = node_type_ids.get(name)
        if not node_type_id:
            available = ", ".join(sorted(node_type_ids.keys()))
            raise ValueError(
                f"Node type '{name}' not found. "
                f"Available types: {available}"
            )
        return node_type_id

    def to_sync_request(
        self,
        workspace_id: int,
        node_type_ids: Dict[str, int]
    ) -> CustomRepositorySyncRequest:
        """Convert to CustomRepositorySyncRequest protobuf."""
        # Resolve node types for all nodes
        protobuf_nodes = []
        for node in self.nodes:
            # Determine node type ID based on resolution strategy
            if self.node_type_resolution == NodeTypeResolution.BY_ID:
                if not node.node_type_id:
                    raise ValueError(
                        f"Node '{node.external_id}': node_type_id required when using BY_ID resolution"
                    )
                node_type_id = node.node_type_id

            elif self.node_type_resolution == NodeTypeResolution.BY_NAME:
                if not node.node_type:
                    raise ValueError(
                        f"Node '{node.external_id}': node_type required when using BY_NAME resolution"
                    )
                node_type_id = self.resolve_node_type(node_type_ids, node.node_type)

            else:  # MIXED
                # Prefer ID, fall back to name
                if node.node_type_id:
                    node_type_id = node.node_type_id
                elif node.node_type:
                    node_type_id = self.resolve_node_type(node_type_ids, node.node_type)
                else:
                    raise ValueError(
                        f"Node '{node.external_id}': either node_type or node_type_id required"
                    )

            protobuf_nodes.append(node.to_protobuf(node_type_id))

        # Convert edges
        protobuf_edges = [edge.to_protobuf() for edge in self.edges]

        # Build request
        return CustomRepositorySyncRequest(
            custom_repository_id=self.repository.id,
            workspace_id=workspace_id,
            nodes=protobuf_nodes,
            edges=protobuf_edges,
            cleanup_stale=self.cleanup_stale
        )

    @classmethod
    def create_template(cls, integration_name: str, repository_name: str) -> "CustomRepositoryConfigurationFile":
        """
        Create a template configuration file with examples. This is useful for getting started or generating a base config.
        """
        config = CustomRepositoryConfigurationFile(
            type="CUSTOM_REPOSITORY_CONFIGURATION_FILE",
            repository=SimpleRepositoryDefinition(
                name=repository_name,
                integration_name=integration_name,
                integration_type="ETL_TOOL",
                integration_description=f"{integration_name} workflow orchestration",
                integration_icon_url="https://example.com/icon.svg",
                node_types=[
                    SimpleCustomNodeType(
                        name="Workflow",
                        name_plural="Workflows"
                    ),
                    SimpleCustomNodeType(
                        name="Task",
                        name_plural="Tasks",
                        allowed_parent_types=["Workflow"]
                    ),
                    SimpleCustomNodeType(
                        name="Column",
                        name_plural="Columns",
                        allowed_parent_types=["Task"],
                        is_column_display=True
                    )
                ]
            ),
            cleanup_stale=True,
            nodes=[
                SimpleRepositorySyncNode(
                    external_id="workflow-1",
                    node_name="Example Workflow",
                    node_type="Workflow",
                    attributes={
                        "owner": "team-name",
                        "environment": "production"
                    }
                ),
                SimpleRepositorySyncNode(
                    external_id="task-1",
                    node_name="Extract Task",
                    node_type="Task",
                    container_external_id="workflow-1",
                    attributes={
                        "description": "Extract data from source"
                    }
                ),
                SimpleRepositorySyncNode(
                    external_id="column-1",
                    node_name="Column 1",
                    node_type="Column",
                    container_external_id="task-1",
                ),
                SimpleRepositorySyncNode(
                    external_id="task-2",
                    node_name="Transform Task",
                    node_type="Task",
                    container_external_id="workflow-1",
                    attributes={
                        "description": "Transform extracted data"
                    }
                ),
                SimpleRepositorySyncNode(
                    external_id="column-2",
                    node_name="Column 2",
                    node_type="Column",
                    container_external_id="task-2",
                )
            ],
            edges=[
                SimpleRepositorySyncEdge(
                    upstream_external_id="column-1",
                    downstream_external_id="column-2"
                )
            ]
        )

        return config
