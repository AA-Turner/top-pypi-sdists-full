import logging
from typing import List, Dict, Tuple, Union, Optional, Set

import typer

from bigeye_sdk.model.enums import MatchType
from bigeye_sdk.functions.search_and_match_functions import wildcard_search, fuzzy_match
from bigeye_sdk.functions.table_functions import fully_qualified_table_to_elements
from bigeye_sdk.generated.com.bigeye.models.generated import (
    Table,
    Integration,
    TableauWorkbook,
    Source,
    Schema,
    Delta,
    TableColumn,
    DataNodeType,
    DataNode,
    LineageRelationship,
    LineageNavigationNodeV2Response, RelationshipType, CreateLineageEdgeV2Request, LineageNodeV2
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.model.lineage_facade import SimpleLineageConfigurationFile, SimpleLineageEdgeRequest, \
    LineageColumnOverride, SimpleCustomNode, LineageConfiguration, SimpleLineageNodeRequest
from bigeye_sdk.model.lineage_graph import LineageGraph, ContainmentNode, IntegrationNode
from bigeye_sdk.model.protobuf_enum_facade import SimpleDataNodeType, SimpleCatalogEntityType

log = get_logger(__file__)


class LineageController:
    def __init__(self, client: DatawatchClient):
        self.client = client
        self.sources_by_name_ix: Dict[str, Source] = self.client.get_sources_by_name()
        self.edge_requests: List[SimpleLineageEdgeRequest] = []
        self.node_requests: List[SimpleLineageNodeRequest] = []
        self.existing_relations: Dict[int, List[int]] = {}
        self.custom_nodes_ix_by_id: Dict[int, LineageNodeV2] = {}
        self.custom_node_search_cache: Dict[str, List[LineageNodeV2]] = {}
        self.lineage_node_ix_by_id: Dict[int, ContainmentNode] = {}
        self.catalog_attributes_request_cache: Dict[int, dict] = {}

    def get_table_by_name(self, entity_name: str) -> Table:
        warehouse, schema, entity_name = fully_qualified_table_to_elements(entity_name)
        table: Table = self.client.get_tables(
            schema=[schema], table_name=[entity_name]
        ).tables[0]
        return table

    def get_tableau_workbook_by_name(
            self, entity_name: str, integration_name: str
    ) -> TableauWorkbook:
        integration: Integration = [
            i for i in self.client.get_integrations() if i.name == integration_name
        ][0]
        workbook = [
            w
            for w in self.client.get_integration_entities(integration_id=integration.id)
            if w.name == entity_name
        ][0]
        return workbook

    def create_node_by_name(self, entity_name: str, integration_name: str) -> DataNode:
        """Create a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            log.info(f"Creating lineage node for table: {entity_name}")
            entity_id = table.id
            node_type = SimpleDataNodeType.TABLE.to_datawatch_object()

        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            log.info(f"Creating lineage node for entity: {workbook.name}")
            entity_id = workbook.id
            node_type = SimpleDataNodeType.TABLEAU.to_datawatch_object()

        return self.client.create_data_node(
            node_type=node_type, node_entity_id=entity_id
        )

    def delete_node_by_name(self, entity_name: str, integration_name: str):
        """Delete a lineage node for an entity"""
        if not integration_name:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting lineage node for table: {table.name}")
        else:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(f"Deleting lineage node for table: {workbook.name}")

        self.client.delete_data_node(data_node_id=node_id)

    def create_relation_from_name(
            self, upstream_table_name: str, downstream_table_name: str
    ) -> LineageRelationship:
        """Create a lineage relationship for 2 entities"""
        warehouse, u_schema, u_table_name = fully_qualified_table_to_elements(
            upstream_table_name
        )
        warehouse, d_schema, d_table_name = fully_qualified_table_to_elements(
            downstream_table_name
        )

        upstream: Table = self.client.get_tables(
            schema=[u_schema], table_name=[u_table_name]
        ).tables[0]
        downstream: Table = self.client.get_tables(
            schema=[d_schema], table_name=[d_table_name]
        ).tables[0]

        log.info(
            f"Creating relationship from {upstream_table_name} to {downstream_table_name}"
        )

        return self.client.create_table_lineage_relationship(
            upstream_data_node_id=upstream.data_node_id,
            downstream_data_node_id=downstream.data_node_id,
        )

    def delete_relationships_by_name(self, entity_name: str, integration_name: str):
        """Deletes all relationships for a node by name."""
        if integration_name:
            workbook = self.get_tableau_workbook_by_name(
                entity_name=entity_name, integration_name=integration_name
            )
            node_id = workbook.data_node_id
            log.info(
                f"Deleting all lineage relationships for workbook: {workbook.name}"
            )
        else:
            table = self.get_table_by_name(entity_name=entity_name)
            node_id = table.data_node_id
            log.info(f"Deleting all lineage relationships for table: {table.name}")

        self.client.delete_lineage_relationship_for_node(data_node_id=node_id)

    def get_schemas_from_selector(self, selector: str) -> List[Schema]:
        # Split selectors into patterns
        source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(selector.lower())

        # Only take source ids that match pattern
        source_ids = [
            source.id
            for source_name, source in self.sources_by_name_ix.items()
            if source_name.lower()
               in wildcard_search(search_string=source_pattern, content=[source_name.lower()])
        ]

        # Only take schemas from those sources that match pattern
        schemas_by_name_ix: Dict[str, Schema] = {
            s.name.lower(): s for s in self.client.get_schemas(warehouse_id=source_ids).schemas
        }
        schemas = [
            schema
            for schema_name, schema in schemas_by_name_ix.items()
            if schema_name
               in wildcard_search(search_string=schema_pattern, content=[schema_name])
        ]

        return schemas

    def get_tables_from_selector(self, selector: str) -> List[Table]:
        # Split selectors into patterns
        source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(selector.lower())
        # Get schemas
        schema_ids = [schema.id for schema in self.get_schemas_from_selector(selector.lower())]

        # Only take tables from those schemas that match pattern
        if not schema_ids:
            log.warning(f"No schemas found for given selector {selector}.")
            return []

        tables_by_id_ix: Dict[int, Table] = {
            t.id: t for t in self.client.get_tables_post(
                schema_ids=schema_ids,
                ignore_fields=False,
                include_data_node_ids=True
            ).tables
        }

        tables = [
            table
            for table_id, table in tables_by_id_ix.items()
            if table.name.lower()
               in wildcard_search(search_string=table_pattern, content=[table.name.lower()])
        ]

        return tables

    @staticmethod
    def infer_relationships_from_lists(
            upstream,
            downstream,
            task: Optional[SimpleCustomNode] = None,
            match_type: MatchType = MatchType.STRICT
    ):
        matching = []
        if match_type == MatchType.STRICT:
            for u in upstream:
                matching_downstream = [d for d in downstream if d.name.lower() == u.name.lower()]
                if matching_downstream:
                    for md in matching_downstream:
                        matching.append((u, md, task))
        elif match_type == MatchType.FUZZY:
            for u in upstream:
                matching_downstream = fuzzy_match(
                    search_string=u.name.lower(),
                    contents=[d.name.lower() for d in downstream],
                    min_match_score=95,
                )
                if matching_downstream:
                    for match in matching_downstream:
                        md_table = [md for md in downstream if md.name.lower() == match[1]]
                        for mdt in md_table:
                            matching.append((u, mdt, task))
        return matching

    def create_edges(self,
                     upstream: Union[Schema, Table, TableColumn, SimpleCustomNode],
                     downstream: Union[Schema, Table, TableColumn, SimpleCustomNode],
                     node_type: DataNodeType):
        if upstream.data_node_id and downstream.data_node_id:
            self.client.create_lineage_edge(upstream_data_node_id=upstream.data_node_id,
                                            downstream_data_node_id=downstream.data_node_id)
        elif upstream.data_node_id and not downstream.data_node_id:
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=upstream.data_node_id,
                                            downstream_data_node_id=d_node.id)
        elif not upstream.data_node_id and downstream.data_node_id:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=u_node.id,
                                            downstream_data_node_id=downstream.data_node_id)
        else:
            u_node = self.client.create_data_node(node_type=node_type, node_entity_id=upstream.id)
            d_node = self.client.create_data_node(node_type=node_type, node_entity_id=downstream.id)
            self.client.create_lineage_edge(upstream_data_node_id=u_node.id,
                                            downstream_data_node_id=d_node.id)

    def create_relations_from_deltas(self, deltas: List[Delta]):
        for d in deltas:
            target_ids = [dc.target_table_id for dc in d.comparison_table_configurations]

            if len(target_ids) > 1:
                log.warning(f'We are unable to determine the proper lineage for deltas with more than 1 target. '
                            f'Please review the `bigeye lineage infer-relations` command for an alternative option.')
            else:
                source_table = self.client.get_tables(ids=[d.source_table.id]).tables[0]
                target_table = self.client.get_tables(ids=target_ids).tables[0]
                try:
                    self.infer_column_level_lineage_from_tables(tables=[(source_table, target_table, None)])
                except Exception as e:
                    log.warning(f'Failed to create lineage relationship between upstream table: {source_table.name} '
                                f'and downstream table: {target_table.name}. Exception: {e}')

    def get_matching_tables_from_selectors(
            self,
            upstream_selector: str,
            downstream_selector: str,
            match_type: MatchType = MatchType.STRICT
    ) -> List[Tuple[Table, Table, SimpleCustomNode]]:
        upstream_tables = self.get_tables_from_selector(upstream_selector)
        downstream_tables = self.get_tables_from_selector(downstream_selector)
        matching_tables: List[Tuple[Table, Table, SimpleCustomNode]] = self.infer_relationships_from_lists(
            upstream=upstream_tables,
            downstream=downstream_tables,
            match_type=match_type
        )
        return matching_tables

    def _search_custom_nodes(self, custom_node: SimpleCustomNode, search_for_container: Optional[bool] = False) -> Optional[LineageNodeV2]:
        if search_for_container:
            search_results = self.client.search_lineage(
                search=custom_node.container_name,
                search_type=DataNodeType.DATA_NODE_TYPE_CUSTOM
            ).results
            lineage_search_results = [sr.lineage_node for sr in search_results]
            matching_result = next(
                (r for r in lineage_search_results if r.node_type == custom_node.node_type
                 and r.node_name == custom_node.container_name and custom_node.container_name in r.catalog_path.path_parts),
                None
            )
            if matching_result:
                custom_node.container_node_id = matching_result.id
        else:
            search_results = self.client.search_lineage(
                search=custom_node.name,
                search_type=custom_node.node_type
            ).results
            lineage_search_results = [sr.lineage_node for sr in search_results]
            matching_result = next(
                (r for r in lineage_search_results if r.node_type == custom_node.node_type
                 and r.node_name == custom_node.name and custom_node.container_name in r.catalog_path.path_parts),
                None
            )
            if matching_result:
                custom_node.data_node_id = matching_result.id

        return matching_result

    def _get_or_set_custom_node(self, custom_node: SimpleCustomNode) -> SimpleCustomNode:
        """Get the data node id of a custom node, if not available then create one and
        return custom task including node id."""

        # Custom Container Node
        custom_container_node = self.custom_nodes_ix_by_id.get(custom_node.container_node_id, None)
        if custom_container_node is None:
            container_search_cache_results = self.custom_node_search_cache.get(custom_node.container_name, None)
            if container_search_cache_results:
                custom_container_node = next(
                    (c for c in container_search_cache_results
                     if c.node_name == custom_node.container_name and c.node_type == DataNodeType.DATA_NODE_TYPE_CUSTOM),
                    None
                )

        if custom_container_node:
            custom_node.container_node_id = custom_container_node.id
        else:
            existing_container = self._search_custom_nodes(custom_node=custom_node, search_for_container=True)
            if existing_container:
                custom_node.container_node_id = existing_container.id
                self.custom_node_search_cache.get(custom_node.container_name, []).append(existing_container)
                self.custom_nodes_ix_by_id[custom_node.container_node_id] = existing_container
            # if task does not exist yet, then create new custom node and assign the data node id
            else:
                new_container = self.client.create_lineage_node(
                    node_name=custom_node.container_name,
                    node_container_name=custom_node.container_name,
                    node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM,
                    icon_url=custom_node.node_icon_url
                )
                custom_node.container_node_id = new_container.id
                self.custom_nodes_ix_by_id[new_container.id] = new_container

        # Custom Node
        existing_custom_node = self.custom_nodes_ix_by_id.get(custom_node.data_node_id, None)
        if existing_custom_node is None:
            search_cache_results = self.custom_node_search_cache.get(custom_node.name, None)
            if search_cache_results:
                existing_custom_node = next(
                    (c for c in search_cache_results
                     if c.node_name == custom_node.name and c.node_type == custom_node.node_type
                     and custom_node.container_name in c.catalog_path.path_parts),
                    None
                )

        if existing_custom_node:
            custom_node.data_node_id = existing_custom_node.id
            entity_id = existing_custom_node.node_entity_id
        else:
            log.info(f"Searching for {custom_node.name} in {custom_node.container_name}...")
            existing_custom_node = self._search_custom_nodes(custom_node=custom_node)
            if existing_custom_node:
                custom_node.data_node_id = existing_custom_node.id
                self.custom_node_search_cache.get(custom_node.name, []).append(existing_custom_node)
                self.custom_nodes_ix_by_id[custom_node.data_node_id] = existing_custom_node
                entity_id = existing_custom_node.node_entity_id
            # if task does not exist yet, then create new custom node and assign the data node id
            else:
                new_task = self.client.create_lineage_node(
                    node_name=custom_node.name,
                    node_container_name=custom_node.container_name,
                    node_type=custom_node.node_type,
                    icon_url=custom_node.node_icon_url
                )
                custom_node.data_node_id = new_task.id
                self.custom_nodes_ix_by_id[custom_node.data_node_id] = new_task
                entity_id = new_task.node_entity_id
                # Add containment association to container and task
                self.client.create_lineage_edge(
                    upstream_data_node_id=custom_node.container_node_id,
                    downstream_data_node_id=custom_node.data_node_id,
                    relationship_type=RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
                )

        if custom_node.metadata is not None:
            posted_metadata = self.catalog_attributes_request_cache.get(entity_id, None)
            if posted_metadata is None or custom_node.metadata != posted_metadata:
                self.client.set_attributes(
                    entity_type=SimpleCatalogEntityType.DATA_NODE_ENTITY,
                    entity_id=entity_id,
                    attributes=custom_node.metadata
                )
                self.catalog_attributes_request_cache[entity_id] = custom_node.metadata

        return custom_node

    def process_all_edge_requests(self, purge_lineage: bool = False):
        count_successful_relations = 0
        count_skipped_relations = 0
        count_failed_relations = 0
        count_deleted_relations = 0

        loading_text = "Purging Lineage..." if purge_lineage else "Generating Lineage..."

        # logging.disable(level=logging.INFO)
        with typer.progressbar(length=len(self.edge_requests), label=loading_text) as progress:
            final_edge_requests: List[CreateLineageEdgeV2Request] = []
            for r in self.edge_requests:
                try:
                    if purge_lineage:
                        "Purging lineage"
                        # TODO update once this is implemented, this current method will deletes containment relationships
                        # https://linear.app/torodata/issue/ONE-2510/[feature-request]-delete-all-relationships-for-a-node-id
                        self.client.delete_lineage_relationship_for_node(data_node_id=r.upstream.data_node_id)
                        # If etl task and purging, then delete all custom objects nested under the container
                        if r.etl_task:
                            custom_node_ids = self._get_custom_node_ids_for_task(r.etl_task)
                            for ln in custom_node_ids.values():
                                self.client.delete_lineage_node(node_id=ln.id)
                        count_deleted_relations += 1
                    elif not r.etl_task:
                        existing_relations = self.existing_relations.get(r.upstream.data_node_id, None)
                        if existing_relations is None or r.downstream.data_node_id not in existing_relations:
                            final_edge_requests.append(CreateLineageEdgeV2Request(
                                upstream_data_node_id=r.upstream.data_node_id,
                                downstream_data_node_id=r.downstream.data_node_id,
                                relationship_type=RelationshipType.RELATIONSHIP_TYPE_LINEAGE
                            ))
                            count_successful_relations += 1
                        else:
                            "Skipping request because the relationship already exists."
                            count_skipped_relations += 1
                    elif r.etl_task:
                        # If etl_task exists, then create a single custom node for etl_task container name
                        # then for every subproject create a custom node
                        # then for all output columns create a custom node entry
                        task = self._get_or_set_custom_node(custom_node=r.etl_task)
                        self._get_existing_relations_for_nodes([task.data_node_id, r.upstream.data_node_id])
                        source_to_etl_deps = self.existing_relations.get(r.upstream.data_node_id, None)
                        etl_downstream_deps = self.existing_relations.get(task.data_node_id, None)

                        if isinstance(r.upstream, TableColumn) or isinstance(r.upstream, SimpleCustomNode):
                            # new column node
                            etl_custom_column_node = SimpleCustomNode(
                                name=r.upstream.name,
                                container_name=r.etl_task.name,
                                container_node_id=task.data_node_id,
                                node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY
                            )
                            etl_column_node = self._get_or_set_custom_node(etl_custom_column_node)
                            # containment relationship of column node with task
                            if etl_column_node.data_node_id not in etl_downstream_deps:
                                final_edge_requests.append(CreateLineageEdgeV2Request(
                                    upstream_data_node_id=task.data_node_id,
                                    downstream_data_node_id=etl_column_node.data_node_id,
                                    relationship_type=RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
                                ))

                            if source_to_etl_deps is None or etl_column_node.data_node_id not in source_to_etl_deps:
                                log.info(f"Adding request for {r.upstream.name} to {etl_column_node.container_name} {etl_column_node.name}")
                                # lineage relationship of column node to upstream dep
                                final_edge_requests.append(CreateLineageEdgeV2Request(
                                    upstream_data_node_id=r.upstream.data_node_id,
                                    downstream_data_node_id=etl_column_node.data_node_id,
                                    relationship_type=RelationshipType.RELATIONSHIP_TYPE_LINEAGE
                                ))
                                count_successful_relations += 1
                            else:
                                "Skipping request because the relationship already exists."
                                count_skipped_relations += 1

                            etl_column_downstream_deps = self.existing_relations.get(etl_column_node.data_node_id, None)
                            if etl_column_downstream_deps is None or r.downstream.data_node_id not in etl_column_downstream_deps:
                                log.info(
                                    f"Adding request for {etl_column_node.container_name} {etl_column_node.name} to {r.downstream.name}")
                                # lineage relationship of column node to downstream dep
                                final_edge_requests.append(CreateLineageEdgeV2Request(
                                    upstream_data_node_id=etl_column_node.data_node_id,
                                    downstream_data_node_id=r.downstream.data_node_id,
                                    relationship_type=RelationshipType.RELATIONSHIP_TYPE_LINEAGE
                                ))
                                count_successful_relations += 1
                            else:
                                "Skipping request because the relationship already exists."
                                count_skipped_relations += 1

                        else:
                            if source_to_etl_deps is None or task.data_node_id not in source_to_etl_deps:
                                self.create_edges(
                                    upstream=r.upstream,
                                    downstream=task,
                                    node_type=r.node_type
                                )
                                count_successful_relations += 1
                            else:
                                "Skipping request because the relationship already exists."
                                count_skipped_relations += 1

                            if etl_downstream_deps is None or r.downstream.data_node_id not in etl_downstream_deps:
                                self.create_edges(
                                    upstream=task,
                                    downstream=r.downstream,
                                    node_type=r.node_type
                                )
                                count_successful_relations += 1
                            else:
                                "Skipping request because the relationship already exists."
                                count_skipped_relations += 1
                    else:
                        "Skipping request because the relationship already exists."
                        count_skipped_relations += 1
                except Exception as e:
                    log.error(
                        f"Failed to create relationship between upstream {r.node_type.name}: {r.upstream.name} and "
                        f"downstream {r.node_type.name}: {r.downstream.name}. Exception {e}"
                    )
                    count_failed_relations += 1

            # Make the lineage request
            cleansed_requests = []
            for r in final_edge_requests:
                if r.upstream_data_node_id != r.downstream_data_node_id:
                    cleansed_requests.append(r)
            self.client.bulk_create_lineage_edges(cleansed_requests)
            progress.update(1)

        # Delete any custom nodes
        if purge_lineage:
            for node_id, node in self.custom_nodes_ix_by_id.items():
                self.client.delete_lineage_node(node_id=node_id)

        logging.disable(level=logging.NOTSET)

        log.info(
            f"\n------------LINEAGE REPORT--------------"
            f"\nCreated {count_successful_relations} edges."
            f"\nSkipped {count_skipped_relations} edges. "
            f"\nDeleted {count_deleted_relations} edges. "
            f"\nFailed {count_failed_relations} edges. "
        )

    def _get_existing_relations_for_nodes(self, node_ids: List[int]) -> None:
        """Get the existing relations for a schema. This is done at the top level to limit the number of requests
        that we have to make."""
        for nid in node_ids:
            if self.existing_relations.get(nid, None) is None:
                downstream_nodes = self.client.get_downstream_nodes(node_id=nid)
                for node in downstream_nodes.nodes.values():
                    # Not sure why but nodes in TableLineageV2Response is a Dict[int, dict].
                    ln_node = LineageNavigationNodeV2Response().from_dict(node)
                    self.existing_relations[ln_node.lineage_node.id] = [d.downstream_id for d in
                                                                        ln_node.downstream_edges]
                    self.custom_node_search_cache.get(ln_node.lineage_node.node_name, []).append(ln_node.lineage_node)

    def _update_search_cache_for_node(self, node_id: int, node_name: Optional[str] = None, scan_upstream: bool = False):
        if node_name is None or self.custom_node_search_cache.get(node_name, None) is None:
            if scan_upstream:
                custom_nodes = self.client.get_downstream_nodes(node_id=node_id, depth=1).nodes
                for node_id, node in custom_nodes.items():
                    ln_node: LineageNavigationNodeV2Response = LineageNavigationNodeV2Response().from_dict(node)
                    for up_edge in ln_node.upstream_edges:
                        if (up_edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
                                and ln_node.lineage_node.node_type in [DataNodeType.DATA_NODE_TYPE_CUSTOM,
                                                                       DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY]):
                            self.custom_nodes_ix_by_id[up_edge.downstream_id] = ln_node.lineage_node
                            if self.custom_node_search_cache.get(ln_node.lineage_node.node_name, None) is None:
                                self.custom_node_search_cache[ln_node.lineage_node.node_name] = [ln_node.lineage_node]
                            else:
                                self.custom_node_search_cache[ln_node.lineage_node.node_name].append(ln_node.lineage_node)
            else:
                custom_nodes = self.client.get_downstream_nodes(node_id=node_id, depth=1).nodes
                for node_id, node in custom_nodes.items():
                    ln_node: LineageNavigationNodeV2Response = LineageNavigationNodeV2Response().from_dict(node)
                    for dn_edge in ln_node.downstream_edges:
                        if (dn_edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT
                                and ln_node.lineage_node.node_type in [DataNodeType.DATA_NODE_TYPE_CUSTOM,
                                                                       DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY]):
                            self.custom_nodes_ix_by_id[dn_edge.upstream_id] = ln_node.lineage_node
                            if self.custom_node_search_cache.get(ln_node.lineage_node.node_name, None) is None:
                                self.custom_node_search_cache[ln_node.lineage_node.node_name] = [ln_node.lineage_node]
                            else:
                                self.custom_node_search_cache[ln_node.lineage_node.node_name].append(ln_node.lineage_node)

    def _execute_lineage_workflow_from_selectors(self, selectors: List[str]):
        source_ids = []
        for s in selectors:
            # Split selectors into patterns
            source_pattern, schema_pattern, table_pattern = fully_qualified_table_to_elements(s)

            # Only take source ids that match pattern
            selector_source_ids = [
                source.id
                for source_name, source in self.sources_by_name_ix.items()
                if source_name
                   in wildcard_search(search_string=source_pattern, content=[source_name])
            ]
            source_ids.extend([ssi for ssi in selector_source_ids if ssi not in source_ids])

        for sid in source_ids:
            self.client.rebuild_source(source_id=sid)

    def _get_custom_node_ids_for_task(self, etl_task: SimpleCustomNode) -> Dict[str, LineageNodeV2]:
        """Get all data node IDs for an etl_task."""

        # First search for the task container, i.e. Python of Airflow
        task = self._search_custom_nodes(custom_node=etl_task)

        # Get all downstream nodes from that task container
        nodes = self.client.get_downstream_nodes(node_id=task.id).nodes

        # Loop through all downstream nodes
        node_response = {}
        task_node_ids = []
        for node in nodes.values():
            ln_node: LineageNavigationNodeV2Response = LineageNavigationNodeV2Response().from_dict(node)
            if ln_node.lineage_node.id == task.id:
                for edge in ln_node.downstream_edges:
                    if edge.relationship_type == RelationshipType.RELATIONSHIP_TYPE_CONTAINMENT:
                        task_node_ids.append(edge.downstream_id)
                        node_response[ln_node.lineage_node.node_name] = ln_node.lineage_node

        for node in nodes.values():
            ln_node: LineageNavigationNodeV2Response = LineageNavigationNodeV2Response().from_dict(node)
            if ln_node.lineage_node.id in task_node_ids:
                node_response[ln_node.lineage_node.node_name] = ln_node.lineage_node

        return node_response

    def _delete_unused_custom_nodes(self, custom_node: SimpleCustomNode, table_to_compare: Table):
        # Check if there are any pre-existing custom column nodes that are no longer present
        # on the table and delete them
        existing_custom_nodes_for_task = self._get_custom_node_ids_for_task(custom_node)
        downstream_column_names = [d_col.name for d_col in table_to_compare.columns]
        nodes_to_delete = [n for node_name, n in existing_custom_nodes_for_task.items()
                           if n.node_name not in downstream_column_names]
        for node in nodes_to_delete:
            self.client.delete_lineage_node(node_id=node.id)

    def create_edges_from_table_names(
            self,
            upstream_table_name: str,
            downstream_table_name: str,
            etl_task_name: Optional[str] = None,
            etl_task_container: Optional[str] = "Python",
            column_overrides: Optional[List[LineageColumnOverride]] = None,
            infer_lineage: bool = True,
            purge_lineage: bool = False
    ):
        """Create a lineage edge for 2 entities"""
        upstream_table: Table = self.get_tables_from_selector(upstream_table_name)[0]
        downstream_table: Table = self.get_tables_from_selector(downstream_table_name)[0]

        etl_task = None
        if etl_task_name:
            etl_task = SimpleCustomNode(name=etl_task_name, container_name=etl_task_container)

        if column_overrides:
            u_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in upstream_table.columns}
            d_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in downstream_table.columns}

            for c_override in column_overrides:
                try:
                    up_column = u_columns_ix_by_name[c_override.upstream_column_name]
                    down_column = d_columns_ix_by_name[c_override.downstream_column_name]
                except KeyError as e:
                    log.warning(
                        f"No column found for provided column override. Please check spelling and try again."
                        f" Exception: {e}")
                    continue

                if up_column.data_node_id != down_column.data_node_id:
                    self.edge_requests.append(
                        SimpleLineageEdgeRequest(
                            upstream=u_columns_ix_by_name[c_override.upstream_column_name],
                            downstream=d_columns_ix_by_name[c_override.downstream_column_name],
                            node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                            etl_task=etl_task
                        )
                    )
            if infer_lineage:
                self.infer_column_level_lineage_from_tables(
                    tables=[(upstream_table, downstream_table, etl_task)]
                )

        elif not column_overrides and not infer_lineage:
            if upstream_table.data_node_id != downstream_table.data_node_id:
                self.edge_requests.append(
                    SimpleLineageEdgeRequest(
                        upstream=upstream_table,
                        downstream=downstream_table,
                        node_type=DataNodeType.DATA_NODE_TYPE_TABLE,
                        etl_task=etl_task
                    )
                )
                self.process_all_edge_requests(purge_lineage=purge_lineage)

        elif infer_lineage and not column_overrides:
            self.infer_column_level_lineage_from_tables(
                tables=[(upstream_table, downstream_table, etl_task)]
            )

    def infer_relations_from_database_tables(self,
                                             r: LineageConfiguration,
                                             process_requests: Optional[bool] = False):
        matching_tables: List[Tuple[Table, Table, SimpleCustomNode]] = []

        upstream_tables: List[Table] = self.get_tables_from_selector(f'{r.upstream_schema_name}.*')
        downstream_tables: List[Table] = self.get_tables_from_selector(f'{r.downstream_schema_name}.*')

        matching_tables_by_name = self.infer_relationships_from_lists(
            upstream=upstream_tables,
            downstream=downstream_tables,
            task=r.etl_task
        )
        matching_tables.extend(matching_tables_by_name)

        # index tables by name for reference later
        upstream_tables_ix_by_name: Dict[str, Table] = {t.name: t for t in upstream_tables}
        downstream_tables_ix_by_name: Dict[str, Table] = {t.name: t for t in downstream_tables}

        if r.table_overrides is not None:
            for t_override in r.table_overrides:
                try:
                    u_table = upstream_tables_ix_by_name[t_override.upstream_table_name]
                    d_table = downstream_tables_ix_by_name[t_override.downstream_table_name]
                    self._update_search_cache_for_node(u_table.data_node_id, scan_upstream=True)
                    self._update_search_cache_for_node(d_table.data_node_id, scan_upstream=True)
                    self._get_existing_relations_for_nodes(node_ids=[u_table.data_node_id, d_table.data_node_id])
                except KeyError as e:
                    log.warning(f"No table found for provided table override. Please check spelling and try again."
                                f" Exception: {e}")
                    continue

                u_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in u_table.columns}
                d_columns_ix_by_name: Dict[str, TableColumn] = {c.name: c for c in d_table.columns}

                # Loop through column exclusions and remove columns from tables if names match
                if t_override.column_name_exclusions is not None:
                    for col_excl in t_override.column_name_exclusions:
                        u_columns_ix_by_name.pop(col_excl, None)
                        d_columns_ix_by_name.pop(col_excl, None)

                    u_table.columns = [col for name, col in u_columns_ix_by_name.items()]
                    d_table.columns = [col for name, col in d_columns_ix_by_name.items()]

                # append to matching tables after removing columns
                # and remove any existing entries if table names are the same
                matched_by_name = (u_table, d_table, r.etl_task)
                if matched_by_name in matching_tables:
                    matching_tables.remove(matched_by_name)
                matching_tables.append((u_table, d_table, t_override.etl_task))

                if t_override.column_overrides is not None:
                    for c_override in t_override.column_overrides:
                        try:
                            up_column = u_columns_ix_by_name[c_override.upstream_column_name]
                            down_column = d_columns_ix_by_name[c_override.downstream_column_name]
                        except KeyError as e:
                            log.warning(
                                f"No column found for provided column override. Please check spelling and try again."
                                f" Exception: {e}")
                            continue

                        if up_column.data_node_id != down_column.data_node_id:
                            self.edge_requests.append(
                                SimpleLineageEdgeRequest(
                                    upstream=u_columns_ix_by_name[c_override.upstream_column_name],
                                    downstream=d_columns_ix_by_name[c_override.downstream_column_name],
                                    node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                                    etl_task=t_override.etl_task,
                                )
                            )

        self.infer_column_level_lineage_from_tables(tables=matching_tables, process_requests=process_requests)

    def infer_column_level_lineage_from_file(
            self, lineage_configuration_file: SimpleLineageConfigurationFile, purge_lineage: bool = False
    ):
        for r in lineage_configuration_file.relations:
            if not r.has_custom:
                self.infer_relations_from_database_tables(r)
            else:
                if r.etl_task is not None:
                    task = self._get_or_set_custom_node(r.etl_task)
                    self._get_existing_relations_for_nodes([task.data_node_id])
                    self._update_search_cache_for_node(task.data_node_id)

                # If upstream is custom, find or create the custom upstream schema node
                if r.has_custom_upstream:
                    up_database, up_schema = r.upstream_schema_name.split(".", maxsplit=1)
                    upstream_task = SimpleCustomNode(name=up_schema, container_name=up_database, node_icon=r.upstream_icon_url)
                    upstream_schema = self._get_or_set_custom_node(upstream_task)
                    self._update_search_cache_for_node(upstream_schema.data_node_id, scan_upstream=True)

                else:
                    upstream_schema = self.get_schemas_from_selector(f'{r.upstream_schema_name}.*')[0]
                    up_schema = upstream_schema.name
                    up_database = upstream_schema.warehouse_name
                    # Database schemas are too large to request lineage for
                    # self._update_search_cache_for_node(upstream_schema.data_node_id, scan_upstream=True)

                # If downstream is custom, find or create the custom downstream schema node
                if r.has_custom_downstream:
                    dn_database, dn_schema = r.downstream_schema_name.split(".", maxsplit=1)
                    downstream_task = SimpleCustomNode(name=dn_schema, container_name=dn_database, node_icon=r.downstream_icon_url)
                    downstream_schema = self._get_or_set_custom_node(downstream_task)
                    self._update_search_cache_for_node(downstream_schema.data_node_id, scan_upstream=True)

                else:
                    downstream_schema = self.get_schemas_from_selector(f'{r.downstream_schema_name}.*')[0]
                    dn_schema = downstream_schema.name
                    dn_database = downstream_schema.warehouse_name
                    # Database schemas are too large to request lineage for
                    # self._update_search_cache_for_node(downstream_schema.data_node_id, scan_upstream=True)

                # For every table override:
                table_node_ids = []
                for t_override in r.table_overrides:
                    # If upstream is custom, find or create the custom upstream table node
                    if r.has_custom_upstream:
                        upstream_table_custom_node = SimpleCustomNode(
                            name=t_override.upstream_table_name,
                            container_name=f"{up_database}.{up_schema}",
                            container_node_id=upstream_schema.data_node_id,
                        )
                        upstream_table = self._get_or_set_custom_node(upstream_table_custom_node)
                    else:
                        upstream_table = next(
                            (
                                t for t in self.get_tables_from_selector(f'{r.upstream_schema_name}.{t_override.upstream_table_name}')
                            ),
                            None
                        )
                        if upstream_table is None:
                            log.warning(
                                f"No table found for provided table override. Please check spelling and try again."
                                f" Upstream table name: {t_override.upstream_table_name}"
                            )
                            continue

                    table_node_ids.append(upstream_table.data_node_id)

                    # If downstream is custom, find or create the custom downstream table node
                    if r.has_custom_downstream:
                        downstream_table_custom_node = SimpleCustomNode(
                            name=t_override.downstream_table_name,
                            container_name=f"{dn_database}.{dn_schema}",
                            container_node_id=downstream_schema.data_node_id
                        )
                        downstream_table = self._get_or_set_custom_node(downstream_table_custom_node)
                    else:
                        downstream_table = next(
                            (
                                t for t in self.get_tables_from_selector(f'{r.downstream_schema_name}.{t_override.downstream_table_name}')
                            ),
                            None
                        )
                        if downstream_table is None:
                            log.warning(
                                f"No table found for provided table override. Please check spelling and try again."
                                f" Downstream table name: {t_override.downstream_table_name}"
                            )
                            continue

                    table_node_ids.append(downstream_table.data_node_id)

                    if not t_override.column_overrides:
                        # if the upstream or downstream tables are custom, then we need to manually create the custom columns
                        # to match the others column structure
                        # if both are custom, then we will ignore columns for now
                        if r.has_custom_upstream and not r.has_custom_downstream:
                            for d_col in downstream_table.columns:
                                upstream_column_custom_node = SimpleCustomNode(
                                    name=d_col.name,
                                    container_name=upstream_table.name,
                                    container_node_id=upstream_table.data_node_id,
                                    node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY
                                )
                                upstream_column = self._get_or_set_custom_node(upstream_column_custom_node)
                                self.edge_requests.append(
                                    SimpleLineageEdgeRequest(
                                        upstream=upstream_column,
                                        downstream=d_col,
                                        node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY,
                                        etl_task=t_override.etl_task
                                    )
                                )
                            # self._delete_unused_custom_nodes(custom_node=upstream_table,
                            #                                  table_to_compare=downstream_table)

                        elif r.has_custom_downstream and not r.has_custom_upstream:
                            for u_col in upstream_table.columns:
                                downstream_column_custom_node = SimpleCustomNode(
                                    name=u_col.name,
                                    container_name=downstream_table.name,
                                    container_node_id=downstream_table.data_node_id,
                                    node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY
                                )
                                downstream_column = self._get_or_set_custom_node(downstream_column_custom_node)
                                self.edge_requests.append(
                                    SimpleLineageEdgeRequest(
                                        upstream=u_col,
                                        downstream=downstream_column,
                                        node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY,
                                        etl_task=t_override.etl_task
                                    )
                                )
                            # self._delete_unused_custom_nodes(custom_node=downstream_table,
                            #                                  table_to_compare=upstream_table)
                        else:
                            self.edge_requests.append(
                                SimpleLineageEdgeRequest(
                                    upstream=upstream_table,
                                    downstream=downstream_table,
                                    node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM,
                                    etl_task=t_override.etl_task
                                )
                            )

                    # For every column override
                    for col_override in t_override.column_overrides:
                        # If upstream is custom, find or create the custom upstream column node (convert to custom_entry)
                        if r.has_custom_upstream:
                            upstream_column_custom_node = SimpleCustomNode(
                                name=col_override.upstream_column_name,
                                container_name=upstream_table.name,
                                container_node_id=upstream_table.data_node_id,
                                node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY
                            )
                            upstream_column = self._get_or_set_custom_node(upstream_column_custom_node)
                        else:
                            upstream_column = next(c for c in upstream_table.columns if c.name == col_override.upstream_column_name)

                        # If downstream is custom, find or create the custom downstream column node (convert to custom_entry)
                        if r.has_custom_downstream:
                            downstream_column_custom_node = SimpleCustomNode(
                                name=col_override.downstream_column_name,
                                container_name=downstream_table.name,
                                container_node_id=downstream_table.data_node_id,
                                node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY
                            )
                            downstream_column = self._get_or_set_custom_node(downstream_column_custom_node)
                        else:
                            downstream_column = next(c for c in downstream_table.columns if c.name == col_override.downstream_column_name)

                        # Create a lineage edge between the upstream and downstream column nodes
                        self.edge_requests.append(
                            SimpleLineageEdgeRequest(
                                upstream=upstream_column,
                                downstream=downstream_column,
                                node_type=DataNodeType.DATA_NODE_TYPE_CUSTOM_ENTRY,
                            )
                        )
                # Get all the relationships for tables and store in index
                self._get_existing_relations_for_nodes(table_node_ids)

        self.process_all_edge_requests(purge_lineage=purge_lineage)

        # TODO remove once this is implemented
        # https://linear.app/torodata/issue/ONE-2510/[feature-request]-delete-all-relationships-for-a-node-id
        if purge_lineage:
            self._execute_lineage_workflow_from_selectors(
                selectors=[f'{r.upstream_schema_name}.*' for r in lineage_configuration_file.relations]
            )
            log.warning(f"Purging lineage currently requires the sources to be re-indexed. This may take a few minutes,"
                        f" do not try to rebuild the lineage until re-indexing process has completed.")

    def infer_column_level_lineage_from_tables(
            self,
            tables: List[Tuple[Union[Table, SimpleCustomNode], Union[Table, SimpleCustomNode], Optional[SimpleCustomNode]]],
            purge_lineage: Optional[bool] = False,
            process_requests: Optional[bool] = True
    ):
        for upstream, downstream, etl_task in tables:
            matching_columns: List[
                Tuple[TableColumn, TableColumn, SimpleCustomNode]] = self.infer_relationships_from_lists(
                upstream=upstream.columns, downstream=downstream.columns, task=etl_task
            )
            if not matching_columns and upstream.data_node_id != downstream.data_node_id:
                self.edge_requests.append(
                    SimpleLineageEdgeRequest(
                        upstream=upstream,
                        downstream=downstream,
                        node_type=DataNodeType.DATA_NODE_TYPE_TABLE,
                        etl_task=etl_task
                    )
                )

            for up_column, down_column, task in matching_columns:
                if up_column.data_node_id != down_column.data_node_id:
                    self.edge_requests.append(
                        SimpleLineageEdgeRequest(
                            upstream=up_column,
                            downstream=down_column,
                            node_type=DataNodeType.DATA_NODE_TYPE_COLUMN,
                            etl_task=task
                        )
                    )

        if process_requests:
            self.process_all_edge_requests(purge_lineage=purge_lineage)

    def search_nodes_for_table(self, table_id: int):
        table = self.client.search_tables(ids=[table_id], ignore_fields=True, include_data_node_ids=True).tables[0]
        self.continuous_search_from_data_node(data_node_id=table.data_node_id)

    def continuous_search_from_data_node(self, data_node_id: int):
        to_search = {data_node_id}
        searched_nodes = set()
        while to_search:
            data_node_id = to_search.pop()
            if data_node_id in searched_nodes:
                continue
                
            searched_nodes.add(data_node_id)
            current_node = self.lineage_node_ix_by_id.get(data_node_id)
            if not current_node:
                graph = self.client.get_lineage_graph_from_data_node(data_node_id=data_node_id, timeout=120)
                current_node = ContainmentNode.build(node_id=data_node_id, graph=graph)
                self.lineage_node_ix_by_id[current_node.id] = current_node

            to_search.update({up_id for up_id in current_node.upstream_objects if up_id not in searched_nodes})
            to_search.update({down_id for down_id in current_node.downstream_objects if down_id not in searched_nodes})
