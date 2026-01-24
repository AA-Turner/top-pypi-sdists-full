from __future__ import annotations

from typing import Optional, Dict, List

from bigeye_sdk.client.datawatch_client import DatawatchClient
from bigeye_sdk.model.custom_repository_facade import (
    CustomRepositoryConfigurationFile,
    SimpleRepositoryDefinition, CatalogDeploymentResult, SimpleRepositorySyncNode, SimpleRepositorySyncEdge,
    SimpleNodeLookup,
)
from bigeye_sdk.generated.com.bigeye.models.generated import (
    CustomRepository,
    CustomNodeType,
)
from bigeye_sdk.generated.com.bigeye.models._generated_root import (
    WorkflowV2Id, DataNodeType,
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.integration_facade import SimpleCustomIntegration, SimpleCustomRepository

log = get_logger(__name__)


class CustomRepositoryController:
    """Controller for managing custom repository synchronization."""

    def __init__(self, client: DatawatchClient):
        self.client = client
        self._node_type_cache: Optional[Dict[str, int]] = None
        self._node_type_cache_by_id: Optional[Dict[int, CustomNodeType]] = None

    def sync_from_config(
        self,
        config: CustomRepositoryConfigurationFile,
        wait_for_completion: bool = False,
        poll_interval: int = 10,
        timeout: int = 600
    ) -> WorkflowV2Id:
        """
        Sync a repository from a configuration file.

        This is the primary method for declarative repository sync. It handles:
        1. Creating/updating the integration type, node types, and repository (if needed)
        2. Node type resolution (name -> ID)
        3. Request building and API submission
        4. Optional workflow tracking

        Args:
            config: Configuration file defining the repository state
            wait_for_completion: If True, blocks until workflow completes
            poll_interval: Seconds between status checks (if waiting)
            timeout: Maximum seconds to wait (if waiting)

        Returns:
            Workflow ID for tracking the sync operation

        Raises:
            ValueError: If configuration is invalid
            Exception: If sync request fails
        """
        log.info(f"Starting sync for repository '{config.repository.name}'")

        # Create/update catalog infrastructure (integration, node types, repository)
        log.info("Upserting catalog infrastructure...")
        deployment = self.upsert_catalog(config.repository)

        # Update config with resolved IDs
        config.repository.id = deployment.repository_id

        # Expand edges with column nodes
        log.info("Expanding edges with automatic column lineage...")
        self._expand_edges_with_columns(config, deployment.node_type_ids)
        log.info(f"After expansion: {len(config.nodes)} nodes, {len(config.edges)} edges")

        # Convert to protobuf request
        request = config.to_sync_request(
            workspace_id=self.client.config.workspace_id,
            node_type_ids=deployment.node_type_ids
        )

        # Submit sync request
        log.info(f"Submitting sync: {len(config.nodes)} nodes, {len(config.edges)} edges")
        response = self.client.sync_custom_repository(request)
        workflow = response.workflow_v2_id

        log.info(f"Sync submitted successfully. Workflow ID: {workflow.workflow_id}")

        # Wait for completion if requested
        if wait_for_completion:
            log.info(f"Waiting for workflow to complete (timeout: {timeout}s)...")
            self.client.wait_for_workflow_v2(
                workflow_id=workflow,
                poll_interval=poll_interval,
                timeout=timeout
            )

        return workflow

    def upsert_catalog(
        self,
        repository_def: SimpleRepositoryDefinition,
    ) -> CatalogDeploymentResult:
        """Create or update the catalog infrastructure for a repository."""
        log.info(f"Upserting catalog for repository '{repository_def.name}'")

        # Build SimpleCustomIntegration for upsert
        repo = SimpleCustomRepository(name=repository_def.name, id=repository_def.id)
        integration = SimpleCustomIntegration(
            name=repository_def.integration_name,
            description=repository_def.integration_description,
            type=repository_def.integration_type,
            icon_url=repository_def.integration_icon_url,
            node_types=repository_def.node_types,
            repositories=[repo]
        )

        deployment_result = self.client.upsert_custom_integration(integration)

        # Build result object
        result = CatalogDeploymentResult(
            integration_type_id=deployment_result.integration_type_id,
            repository_id=deployment_result.get_repository_id(repository_def.name),
            node_type_ids=deployment_result.node_type_ids,
            created=deployment_result.created,
            updated=deployment_result.updated
        )

        log.info(f"Catalog upserted successfully. Integration: {result.integration_type_id}, "
                 f"Repository: {result.repository_id}, Node types: {len(result.node_type_ids)}")

        return result

    def _find_column_node_type(self, config: CustomRepositoryConfigurationFile) -> Optional[str]:
        """
        Find the first node type in repository definition with is_column_display=True.

        Args:
            config: Configuration file with repository definition

        Returns:
            Node type name, or None if not found
        """
        for node_type in config.repository.node_types:
            if node_type.is_column_display:
                return node_type.name
        return None

    def _is_table_and_get_columns(self, node_id: int) -> Optional[List[Dict]]:
        """
        Check if node_id points to a DATA_NODE_TYPE_TABLE and get its columns.

        Args:
            node_id: DataNode ID to check

        Returns:
            List of column info dicts with keys: id, name, data_node_id
            Returns None if node is not a table
            Returns empty list if table has no columns

        Raises:
            ValueError: If node cannot be fetched or columns cannot be queried
        """
        try:
            data_node = self.client.get_data_node_by_id(node_id)
        except Exception as e:
            log.error(f"Failed to fetch data node {node_id}: {e}")
            raise ValueError(
                f"Edge expansion failed: Could not fetch node information for node_id={node_id}. "
                f"Ensure the node exists and is accessible."
            ) from e

        # Check if this is a table node
        if data_node.node_type != DataNodeType.DATA_NODE_TYPE_TABLE:
            return None

        # Query columns for this table
        try:
            response = self.client.get_columns(table_ids=[data_node.node_entity_id])
        except Exception as e:
            log.error(f"Failed to fetch columns for table {data_node.node_entity_id}: {e}")
            raise ValueError(
                f"Edge expansion failed: Could not fetch columns for table (node_id={node_id}). "
                f"Ensure the table has been indexed in the catalog."
            ) from e

        if not response.columns:
            return []

        return [
            {
                'id': col.column.id,
                'name': col.column.name,
                'data_node_id': col.column.data_node_id
            }
            for col in response.columns
        ]

    def _node_exists(self, external_id: str, config: CustomRepositoryConfigurationFile) -> bool:
        """
        Check if node with external_id already exists in config.

        Args:
            external_id: External ID to check
            config: Configuration file

        Returns:
            True if node exists, False otherwise
        """
        return any(node.external_id == external_id for node in config.nodes)

    def _generate_column_nodes_and_edges(
        self,
        parent_external_id: str,
        columns: List[Dict],
        column_node_type: str,
        config: CustomRepositoryConfigurationFile,
        container_external_id: Optional[str] = None
    ) -> List:
        """
        Generate column nodes under a parent entity.

        Args:
            parent_external_id: External ID used for column node IDs (typically table node_id)
            columns: List of column info dicts
            column_node_type: Node type name for column nodes
            config: Configuration to check for existing nodes
            container_external_id: External ID of the container node (defaults to parent_external_id)

        Returns:
            List of SimpleRepositorySyncNode objects
        """
        # If no container specified, use parent as container
        if container_external_id is None:
            container_external_id = parent_external_id

        nodes = []
        for col in columns:
            external_id = f"{parent_external_id}__column__{col['name']}"

            # Check if node already exists
            if self._node_exists(external_id, config):
                log.warning(
                    f"Column external_id '{external_id}' already exists in nodes. "
                    f"Skipping duplicate node creation."
                )
                continue

            nodes.append(SimpleRepositorySyncNode(
                external_id=external_id,
                node_name=col['name'],
                node_type=column_node_type,
                container_external_id=container_external_id
            ))

        return nodes

    def _expand_edges_with_columns(
        self,
        config: CustomRepositoryConfigurationFile,
        node_type_ids: Dict[str, int]
    ) -> None:
        """
        Expand edges that have expand_upstream or expand_downstream flags set.

        For each edge with expansion enabled:
        1. Check if the referenced node is a table (DATA_NODE_TYPE_TABLE)
        2. Query columns for that table via get_columns() API
        3. Find the column display node type from repository definition
        4. Generate column nodes with external_id format: {parent_id}__column__{column_name}
        5. Generate column-to-column edges

        Modifies config.nodes and config.edges in place.

        Args:
            config: Configuration file to expand
            node_type_ids: Mapping of node type names to IDs

        Raises:
            ValueError: If expansion cannot be performed (missing column type, invalid node, etc)
        """
        # Find column node type
        column_node_type = self._find_column_node_type(config)
        if column_node_type is None:
            # Check if any edges actually need expansion
            needs_expansion = any(
                edge.expand_upstream or edge.expand_downstream
                for edge in config.edges
            )
            if needs_expansion:
                raise ValueError(
                    "Edge expansion failed: No node type with is_column_display=True found in repository. "
                    "Define a column node type with is_column_display=True to enable expansion."
                )
            # No expansion needed, return early
            return

        expanded_nodes = []
        expanded_edges = []
        processed_tables = {}  # Cache: external_id -> List[column_info]

        for edge in config.edges:
            # Handle passthrough edges (table -> activity -> table)
            if edge.passthrough_external_id:
                self._process_passthrough_edge(
                    edge, config, column_node_type, expanded_nodes, expanded_edges, processed_tables
                )
                continue

            if not edge.expand_upstream and not edge.expand_downstream:
                continue

            # Process upstream expansion
            upstream_columns = []
            upstream_parent_id = None
            if edge.expand_upstream:
                if edge.upstream_external_id:
                    raise ValueError(
                        "Edge expansion failed: expand_upstream=True requires upstream_node with node_id. "
                        "Cannot expand repository nodes (upstream_external_id)."
                    )

                if not edge.upstream_node or not edge.upstream_node.node_id:
                    raise ValueError(
                        "Edge expansion failed: expand_upstream=True requires upstream_node with node_id."
                    )

                node_id = edge.upstream_node.node_id
                upstream_parent_id = str(node_id)

                # Check cache
                if upstream_parent_id not in processed_tables:
                    columns = self._is_table_and_get_columns(node_id)
                    if columns is None:
                        raise ValueError(
                            f"Edge expansion failed: upstream node (node_id={node_id}) "
                            f"is not a table. Only DATA_NODE_TYPE_TABLE can be expanded."
                        )

                    if len(columns) == 0:
                        log.warning(
                            f"Skipping expansion for edge: table node_id={node_id} has no columns. "
                            f"No column nodes will be created."
                        )
                        continue

                    processed_tables[upstream_parent_id] = columns

                upstream_columns = processed_tables[upstream_parent_id]

            # Process downstream expansion
            downstream_columns = []
            downstream_parent_id = None
            if edge.expand_downstream:
                if edge.downstream_external_id:
                    raise ValueError(
                        "Edge expansion failed: expand_downstream=True requires downstream_node with node_id. "
                        "Cannot expand repository nodes (downstream_external_id)."
                    )

                if not edge.downstream_node or not edge.downstream_node.node_id:
                    raise ValueError(
                        "Edge expansion failed: expand_downstream=True requires downstream_node with node_id."
                    )

                node_id = edge.downstream_node.node_id
                downstream_parent_id = str(node_id)

                # Check cache
                if downstream_parent_id not in processed_tables:
                    columns = self._is_table_and_get_columns(node_id)
                    if columns is None:
                        raise ValueError(
                            f"Edge expansion failed: downstream node (node_id={node_id}) "
                            f"is not a table. Only DATA_NODE_TYPE_TABLE can be expanded."
                        )

                    if len(columns) == 0:
                        log.warning(
                            f"Skipping expansion for edge: table node_id={node_id} has no columns. "
                            f"No column nodes will be created."
                        )
                        continue

                    processed_tables[downstream_parent_id] = columns

                downstream_columns = processed_tables[downstream_parent_id]

            # Generate column nodes
            if upstream_columns:
                # Upstream columns should be contained by the downstream node
                container_id = edge.downstream_external_id if edge.downstream_external_id else None
                nodes = self._generate_column_nodes_and_edges(
                    upstream_parent_id, upstream_columns, column_node_type, config, container_id
                )
                expanded_nodes.extend(nodes)

            if downstream_columns:
                # Downstream columns should be contained by the upstream node
                container_id = edge.upstream_external_id if edge.upstream_external_id else None
                nodes = self._generate_column_nodes_and_edges(
                    downstream_parent_id, downstream_columns, column_node_type, config, container_id
                )
                expanded_nodes.extend(nodes)

            # Generate edges
            if upstream_columns and downstream_columns:
                # Both sides expanded: cartesian product
                for upstream_col in upstream_columns:
                    for downstream_col in downstream_columns:
                        upstream_ext_id = f"{upstream_parent_id}__column__{upstream_col['name']}"
                        downstream_ext_id = f"{downstream_parent_id}__column__{downstream_col['name']}"

                        expanded_edges.append(SimpleRepositorySyncEdge(
                            upstream_external_id=upstream_ext_id,
                            downstream_external_id=downstream_ext_id,
                            relationship_type="LINEAGE"
                        ))
            elif upstream_columns:
                # Only upstream expanded: connect to downstream node
                downstream_ref = edge.downstream_external_id or str(edge.downstream_node.node_id)
                for upstream_col in upstream_columns:
                    upstream_ext_id = f"{upstream_parent_id}__column__{upstream_col['name']}"

                    if edge.downstream_external_id:
                        expanded_edges.append(SimpleRepositorySyncEdge(
                            upstream_external_id=upstream_ext_id,
                            downstream_external_id=edge.downstream_external_id,
                            relationship_type="LINEAGE"
                        ))
                    else:
                        expanded_edges.append(SimpleRepositorySyncEdge(
                            upstream_external_id=upstream_ext_id,
                            downstream_node=edge.downstream_node,
                            relationship_type="LINEAGE"
                        ))
            elif downstream_columns:
                # Only downstream expanded: connect from upstream node
                upstream_ref = edge.upstream_external_id or str(edge.upstream_node.node_id)
                for downstream_col in downstream_columns:
                    downstream_ext_id = f"{downstream_parent_id}__column__{downstream_col['name']}"

                    if edge.upstream_external_id:
                        expanded_edges.append(SimpleRepositorySyncEdge(
                            upstream_external_id=edge.upstream_external_id,
                            downstream_external_id=downstream_ext_id,
                            relationship_type="LINEAGE"
                        ))
                    else:
                        expanded_edges.append(SimpleRepositorySyncEdge(
                            upstream_node=edge.upstream_node,
                            downstream_external_id=downstream_ext_id,
                            relationship_type="LINEAGE"
                        ))

        # Add expanded nodes and edges to config
        config.nodes.extend(expanded_nodes)
        config.edges.extend(expanded_edges)

        # Remove passthrough edges (they're just templates, the actual edges are in expanded_edges)
        original_edge_count = len(config.edges)
        config.edges = [edge for edge in config.edges if not edge.passthrough_external_id]
        passthrough_edges_removed = original_edge_count - len(config.edges)

        if passthrough_edges_removed > 0:
            log.info(f"Removed {passthrough_edges_removed} passthrough template edge(s)")

        log.info(f"Expansion complete: added {len(expanded_nodes)} column nodes and {len(expanded_edges)} edges")

    def _process_passthrough_edge(
        self,
        edge,
        config: CustomRepositoryConfigurationFile,
        column_node_type: str,
        expanded_nodes: List,
        expanded_edges: List,
        processed_tables: Dict[str, List[Dict]]
    ) -> None:
        """
        Process a passthrough edge (table -> activity -> table).

        Creates column nodes under the passthrough entity and maps matching columns
        by name from upstream to downstream through the passthrough.

        Uses table IDs to query actual column DataNode IDs and creates edges directly
        to the existing column nodes in the warehouse.

        Args:
            edge: Edge with passthrough_external_id set
            config: Configuration file
            column_node_type: Node type for column nodes
            expanded_nodes: List to append new nodes to
            expanded_edges: List to append new edges to
            processed_tables: Cache of table columns (now keyed by table_id with DataNode IDs)

        Raises:
            ValueError: If edge is invalid for passthrough
        """
        # Validate passthrough edge
        if not edge.upstream_node or not edge.upstream_node.table_id:
            raise ValueError(
                f"Passthrough edge requires upstream_node with table_id. "
                f"Got: {edge.upstream_node}"
            )

        if not edge.downstream_node or not edge.downstream_node.table_id:
            raise ValueError(
                f"Passthrough edge requires downstream_node with table_id. "
                f"Got: {edge.downstream_node}"
            )

        passthrough_id = edge.passthrough_external_id

        # Check that passthrough node exists
        if not self._node_exists(passthrough_id, config):
            raise ValueError(
                f"Passthrough node '{passthrough_id}' not found in config nodes. "
                f"Define the passthrough node before using it in edges."
            )

        # Get columns from upstream table using get_tables_post
        upstream_table_id = edge.upstream_node.table_id
        upstream_parent_id = str(upstream_table_id)

        if upstream_parent_id not in processed_tables:
            log.info(f"Querying upstream table (table_id={upstream_table_id}) for column DataNode IDs")
            try:
                table_response = self.client.get_tables_post(
                    table_ids=[upstream_table_id],
                    ignore_fields=False,
                    include_data_node_ids=True
                )
            except Exception as e:
                raise ValueError(
                    f"Failed to query upstream table (table_id={upstream_table_id}): {e}"
                )

            if not table_response.tables or len(table_response.tables) == 0:
                raise ValueError(
                    f"Upstream table (table_id={upstream_table_id}) not found"
                )

            table = table_response.tables[0]
            if not table.columns or len(table.columns) == 0:
                log.warning(
                    f"Skipping passthrough for edge: upstream table (table_id={upstream_table_id}) has no columns."
                )
                return

            # Extract column info with DataNode IDs
            columns = [{'name': col.name, 'data_node_id': col.data_node_id} for col in table.columns]
            processed_tables[upstream_parent_id] = columns

        upstream_columns = processed_tables[upstream_parent_id]

        # Get columns from downstream table using get_tables_post
        downstream_table_id = edge.downstream_node.table_id
        downstream_parent_id = str(downstream_table_id)

        if downstream_parent_id not in processed_tables:
            log.info(f"Querying downstream table (table_id={downstream_table_id}) for column DataNode IDs")
            try:
                table_response = self.client.get_tables_post(
                    table_ids=[downstream_table_id],
                    ignore_fields=False,
                    include_data_node_ids=True
                )
            except Exception as e:
                raise ValueError(
                    f"Failed to query downstream table (table_id={downstream_table_id}): {e}"
                )

            if not table_response.tables or len(table_response.tables) == 0:
                raise ValueError(
                    f"Downstream table (table_id={downstream_table_id}) not found"
                )

            table = table_response.tables[0]
            if not table.columns or len(table.columns) == 0:
                log.warning(
                    f"Skipping passthrough for edge: downstream table (table_id={downstream_table_id}) has no columns."
                )
                return

            # Extract column info with DataNode IDs
            columns = [{'name': col.name, 'data_node_id': col.data_node_id} for col in table.columns]
            processed_tables[downstream_parent_id] = columns

        downstream_columns = processed_tables[downstream_parent_id]

        # Build column name mappings
        upstream_col_by_name = {col['name']: col for col in upstream_columns}
        downstream_col_by_name = {col['name']: col for col in downstream_columns}

        # Get union of all column names
        all_column_names = set(upstream_col_by_name.keys()) | set(downstream_col_by_name.keys())

        log.info(f"Passthrough mapping: {len(upstream_columns)} upstream columns, "
                 f"{len(downstream_columns)} downstream columns, "
                 f"{len(all_column_names)} unique names")

        # Create ONLY passthrough column nodes (not warehouse column nodes - those already exist)
        passthrough_columns_created = []
        for col_name in all_column_names:
            passthrough_col_external_id = f"{passthrough_id}__column__{col_name}"

            # Check if node already exists
            if self._node_exists(passthrough_col_external_id, config):
                log.debug(f"Passthrough column '{passthrough_col_external_id}' already exists, skipping")
                passthrough_columns_created.append(col_name)
                continue

            expanded_nodes.append(SimpleRepositorySyncNode(
                external_id=passthrough_col_external_id,
                node_name=col_name,
                node_type=column_node_type,
                container_external_id=passthrough_id
            ))
            passthrough_columns_created.append(col_name)

        # Create edges: upstream column DataNode -> passthrough -> downstream column DataNode
        # Uses node_id references to existing warehouse columns, not external_id
        edges_created = 0
        for col_name in passthrough_columns_created:
            passthrough_col_external_id = f"{passthrough_id}__column__{col_name}"

            # Create upstream column DataNode -> passthrough edge (if upstream column exists)
            if col_name in upstream_col_by_name:
                upstream_col_data_node_id = upstream_col_by_name[col_name]['data_node_id']
                expanded_edges.append(SimpleRepositorySyncEdge(
                    upstream_node=SimpleNodeLookup(node_id=upstream_col_data_node_id),
                    downstream_external_id=passthrough_col_external_id,
                    relationship_type="LINEAGE"
                ))
                edges_created += 1

            # Create passthrough -> downstream column DataNode edge (if downstream column exists)
            if col_name in downstream_col_by_name:
                downstream_col_data_node_id = downstream_col_by_name[col_name]['data_node_id']
                expanded_edges.append(SimpleRepositorySyncEdge(
                    upstream_external_id=passthrough_col_external_id,
                    downstream_node=SimpleNodeLookup(node_id=downstream_col_data_node_id),
                    relationship_type="LINEAGE"
                ))
                edges_created += 1

        log.info(f"Passthrough complete: created {len(passthrough_columns_created)} passthrough columns "
                 f"and {edges_created} edges (warehouse_col->passthrough->warehouse_col)")

    def get_repository(self, repository_id: int) -> CustomRepository:
        """Get a custom repository by ID."""
        repositories = self.client.get_custom_repositories()
        for repo in repositories.repositories:
            if repo.id == repository_id:
                return repo
        raise ValueError(f"Repository {repository_id} not found")

    def list_repositories(self) -> List[CustomRepository]:
        """List all custom repositories in the workspace."""
        response = self.client.get_custom_repositories()
        return response.repositories

    def get_node_types(self, refresh_cache: bool = False) -> List[CustomNodeType]:
        """Get all custom node types."""
        if refresh_cache or self._node_type_cache_by_id is None:
            response = self.client.get_custom_node_types()
            self._node_type_cache_by_id = {nt.id: nt for nt in response.types}
            self._node_type_cache = {nt.name: nt.id for nt in response.types}

        return list(self._node_type_cache_by_id.values())

    def get_node_type_by_name(self, name: str) -> Optional[CustomNodeType]:
        """Get a node type by name."""
        self.get_node_types()  # Ensure cache is populated
        node_type_id = self._node_type_cache.get(name)
        if node_type_id:
            return self._node_type_cache_by_id.get(node_type_id)
        return None

    def get_node_type_id(self, name: str) -> int:
        """Get a node type ID by name."""
        self.get_node_types()  # Ensure cache is populated
        node_type_id = self._node_type_cache.get(name)
        if not node_type_id:
            available = ", ".join(sorted(self._node_type_cache.keys()))
            raise ValueError(
                f"Node type '{name}' not found. "
                f"Available types: {available}"
            )
        return node_type_id
