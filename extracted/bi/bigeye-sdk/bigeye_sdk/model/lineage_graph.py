import abc
from abc import abstractmethod
from typing import Dict, Set, Union, Optional
from collections import defaultdict

from bigeye_sdk.model.protobuf_enum_facade import SimpleIntegrationPartner
from pydantic.v1 import Field, BaseModel

from bigeye_sdk.generated.com.bigeye.models.generated import TableLineageV2Response, RelationshipType, \
    LineageNavigationNodeV2Response, LineageNodeV2, DataNodeType, IntegrationPartner

bi_tool_partners = [
    IntegrationPartner.INTEGRATION_PARTNER_TABLEAU,
    IntegrationPartner.INTEGRATION_PARTNER_POWERBI,
    IntegrationPartner.INTEGRATION_PARTNER_LOOKER
]


class LineageNode(BaseModel):
    id: int
    name: str
    node_entity_id: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class ColumnNode(LineageNode):
    parent_id: int
    upstream_objects_ix: Dict[int, Set[int]] = defaultdict(set)
    downstream_objects_ix: Dict[int, Set[int]] = defaultdict(set)

    def add_upstream_object(self, upstream_connection: LineageNavigationNodeV2Response):
        for edge in upstream_connection.upstream_edges:
            if edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT:
                self.upstream_objects_ix[edge.upstream_id].add(edge.downstream_id)

    def add_downstream_object(self, downstream_connection: LineageNavigationNodeV2Response):
        for edge in downstream_connection.upstream_edges:
            if edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT:
                self.downstream_objects_ix[edge.upstream_id].add(edge.downstream_id)


class ContainmentNode(LineageNode, abc.ABC):
    upstream_objects: Set[int] = Field(default_factory=lambda: set({}))
    downstream_objects: Set[int] = Field(default_factory=lambda: set({}))
    upstream_connections: Dict[int, ColumnNode] = Field(default_factory=lambda: {})
    downstream_connections: Dict[int, ColumnNode] = Field(default_factory=lambda: {})

    @abstractmethod
    def is_origin(self) -> bool:
        pass

    @abstractmethod
    def is_terminus(self) -> bool:
        pass

    @abstractmethod
    def fully_qualified_name(self, column_name: str) -> str:
        pass

    @classmethod
    def build(cls, node_id: int, graph: TableLineageV2Response) -> Union["TableNode", "IntegrationNode"]:
        graph.nodes = {int(k): v for k, v in graph.nodes.items()}
        navigation_node = graph.nodes.get(node_id)
        containment_node = cls.__containment_node(node=navigation_node.lineage_node)

        containment_node.build_connections(graph=graph, nav_node=navigation_node)
        return containment_node

    @staticmethod
    def __containment_node(node: LineageNodeV2) -> Union["TableNode", "IntegrationNode"]:
        if node.node_type == DataNodeType.DATA_NODE_TYPE_TABLE:
            containment_node = TableNode(
                id=node.id,
                name=node.node_name,
                node_entity_id=node.node_entity_id,
                source_id=node.source.id,
                schema_name=node.catalog_path.schema_name
            )
        else:
            containment_node = IntegrationNode(
                id=node.id,
                name=node.node_name,
                node_entity_id=node.node_entity_id,
                partner_type=node.source.integration_partner,
                partner_name=SimpleIntegrationPartner.from_datawatch_object(node.source.integration_partner).lower()
            )
            containment_node.is_bi_tool = containment_node.partner_type in bi_tool_partners
        return containment_node

    def add_upstream_object(self, upstream_connection: LineageNavigationNodeV2Response):
        containment_object_id = [
            e.upstream_id
            for e in
            upstream_connection.upstream_edges
            if e.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
        ][0]
        self.upstream_objects.add(containment_object_id)

    def add_downstream_object(self, downstream_connection: LineageNavigationNodeV2Response):
        containment_object_id = [
            e.upstream_id
            for e in
            downstream_connection.upstream_edges
            if e.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
        ][0]
        self.downstream_objects.add(containment_object_id)

    def build_connections(self, graph: TableLineageV2Response, nav_node: LineageNavigationNodeV2Response):
        integration_partner = nav_node.lineage_node.source.integration_partner
        if integration_partner and integration_partner in bi_tool_partners:
            lineage_object_ids = {
                e.downstream_id
                for e in
                nav_node.downstream_edges
                if e.relationship_type == RelationshipType.RELATIONSHIP_TYPE_LINEAGE
            }
            parent_node_id = next((e.upstream_id for e in nav_node.upstream_edges
                                   if e.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT), 0)
            if parent_node_id:
                entity_id = graph.nodes.get(parent_node_id).lineage_node.node_entity_id
                self.parent_entity_id = entity_id
            self.downstream_objects.update(lineage_object_ids)
        else:
            for edge in nav_node.downstream_edges:
                # Only interested in column level lineage
                if edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT:
                    column_nav_node = graph.nodes.get(edge.downstream_id)
                    self.build_downstream_connections(graph=graph, column_nav_node=column_nav_node)
                    self.build_upstream_connections(graph=graph, column_nav_node=column_nav_node)

    def build_downstream_connections(self,
                                     graph: TableLineageV2Response,
                                     column_nav_node: LineageNavigationNodeV2Response):

        for col_edge in column_nav_node.downstream_edges:
            if col_edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_LINEAGE:
                column_connection = graph.nodes.get(col_edge.downstream_id)
                column_node = self.downstream_connections.get(
                    column_nav_node.lineage_node.id,
                    ColumnNode(
                        id=column_nav_node.lineage_node.id,
                        name=column_nav_node.lineage_node.node_name,
                        node_entity_id=column_nav_node.lineage_node.node_entity_id,
                        parent_id=self.id
                    )
                )
                integration_partner = column_connection.lineage_node.source.integration_partner
                if integration_partner and integration_partner in bi_tool_partners:
                    self.downstream_objects.add(column_connection.lineage_node.id)
                    column_node.downstream_objects_ix[column_connection.lineage_node.id].add(
                        column_connection.lineage_node.id)
                else:
                    self.add_downstream_object(downstream_connection=column_connection)
                    column_node.add_downstream_object(downstream_connection=column_connection)
                self.downstream_connections[column_nav_node.lineage_node.id] = column_node

    def build_upstream_connections(self,
                                   graph: TableLineageV2Response,
                                   column_nav_node: LineageNavigationNodeV2Response):

        for col_edge in column_nav_node.upstream_edges:
            if col_edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_LINEAGE:
                column_connection = graph.nodes.get(col_edge.upstream_id)
                if column_connection.upstream_edges:
                    self.add_upstream_object(upstream_connection=column_connection)
                column_node = self.upstream_connections.get(
                    column_nav_node.lineage_node.id,
                    ColumnNode(
                        id=column_nav_node.lineage_node.id,
                        name=column_nav_node.lineage_node.node_name,
                        node_entity_id=column_nav_node.lineage_node.node_entity_id,
                        parent_id=self.id
                    )
                )
                column_node.add_upstream_object(upstream_connection=column_connection)
                self.upstream_connections[column_nav_node.lineage_node.id] = column_node


class TableNode(ContainmentNode):
    source_id: int
    schema_name: str

    def is_origin(self) -> bool:
        return len(self.upstream_connections) == 0

    def is_terminus(self) -> bool:
        return len(self.downstream_connections) == 0

    def fully_qualified_name(self, column_name: Optional[str] = None) -> str:
        return f"{self.schema_name}.{self.name}.{column_name}" if column_name else f"{self.schema_name}.{self.name}"


class IntegrationNode(ContainmentNode):
    partner_type: IntegrationPartner
    partner_name: str
    is_bi_tool: bool = False
    parent_entity_id: int = 0

    def is_origin(self) -> bool:
        return len(self.upstream_objects) == 0 if not self.is_bi_tool else False

    def is_terminus(self) -> bool:
        return len(self.downstream_objects) == 0

    def fully_qualified_name(self, column_name: Optional[str] = None) -> str:
        return (f"{self.partner_name}.{self.name}.{column_name}"
                if not self.is_bi_tool and column_name else f"{self.partner_name}.{self.name}")


class LineageGraph(BaseModel):
    node_index: Dict[int, ContainmentNode]
    contains_bi_tool: bool = False

    @classmethod
    def begin(cls, node_index: Dict[int, ContainmentNode]) -> "LineageGraph":
        return LineageGraph(node_index=node_index)
