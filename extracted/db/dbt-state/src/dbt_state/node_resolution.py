from __future__ import annotations

import sys
import typing as t
from dataclasses import replace
from functools import cached_property

from dbt.adapters.base.relation import BaseRelation
from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.manifest import Manifest, SourceDefinition
from dbt.contracts.graph.nodes import (
    ManifestNode,
    ManifestSQLNode,
    ModelNode,
    SeedNode,
    SnapshotNode,
)

try:
    from dbt.artifacts.resources.v1.components import DeferRelation
except ImportError:
    from dbt.contracts.graph.nodes import DeferRelation  # type: ignore[no-redef]
from query_cache_common.models import shared_models
from query_cache_common.models.services import execution_service_models
from sqlglot import exp
from sqlglot.errors import SqlglotError

from dbt_state import events
from dbt_state.adapters import BaseAdapterExtension
from dbt_state.config import RunCacheConfig
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.profiles import Profiles
from dbt_state.relation import DeferredRelationResolver
from dbt_state.utils import DBT_VERSION


class NodeResolution:
    """Resolves dbt manifest nodes to warehouse tables, including deferred (prod) tables."""

    def __init__(
        self,
        manifest: Manifest,
        adapter_ext: BaseAdapterExtension,
        deferred_relation_resolver: t.Optional[DeferredRelationResolver],
        profiles: Profiles,
        config: RuntimeConfig,
        run_cache_config: RunCacheConfig,
        query_cache_client: QueryCacheGrpcClient,
    ) -> None:
        self._manifest = manifest
        self._adapter_ext = adapter_ext
        self._deferred_relation_resolver = deferred_relation_resolver
        self._profiles = profiles
        self._config = config
        self._run_cache_config = run_cache_config
        self._query_cache_client = query_cache_client

    @cached_property
    def selected_resource_ids(self) -> t.Set[str]:
        from dbt.selected_resources import SELECTED_RESOURCES

        return set(SELECTED_RESOURCES)

    @property
    def defer_enabled(self) -> bool:
        if self._deferred_relation_resolver is None:
            return False
        # defer should always be considered enabled (for RunCache plugin purposes) unless --no-defer was explicitly provided by the user
        # note that we have to check sys.argv because:
        # - the original cli args are not available on RuntimeConfig
        # - RuntimeConfig.args.defer defaults to False which means we cannot tell the difference between the default and a explicitly supplied --no-defer argument
        return "--no-defer" not in sys.argv

    @property
    def dialect(self) -> str:
        """The sqlglot dialect for the warehouse."""
        return self._adapter_ext.dialect

    def node_to_table(self, node: ManifestNode | SourceDefinition) -> exp.Table:
        return self._adapter_ext._node_to_table(node)  # noqa: SLF001

    def sql(self, expr: exp.Expr, copy: bool = False) -> str:
        return self._adapter_ext._sql(expr, copy=copy)  # noqa: SLF001

    def iter_selected_nodes(self, selected_ids: t.Set[str]) -> t.Iterator[ModelNode | SnapshotNode]:
        """Yield model/snapshot nodes matching selected_ids"""
        for node in self._manifest.nodes.values():
            if not isinstance(node, (ModelNode, SnapshotNode)):
                continue
            if selected_ids and node.unique_id not in selected_ids:
                continue
            yield node

    def resolve_deps(self, node: ManifestSQLNode) -> t.Tuple[t.Set[str], t.Set[str]]:
        """Return model dependency IDs and source IDs, resolving transitively through ephemeral models."""
        model_ids: t.Set[str] = set()
        source_ids: t.Set[str] = set()
        stack: t.List[str] = []
        for n in getattr(node.depends_on, "nodes", []):
            if n.startswith("source."):
                source_ids.add(n)
            else:
                stack.append(n)
        visited: t.Set[str] = set()
        while stack:
            dep_id = stack.pop()
            if dep_id in visited:
                continue
            visited.add(dep_id)
            dep_node = self._manifest.nodes.get(dep_id)
            if isinstance(dep_node, ModelNode) and dep_node.get_materialization() == "ephemeral":
                for n in getattr(dep_node.depends_on, "nodes", []):
                    if n.startswith("source."):
                        source_ids.add(n)
                    else:
                        stack.append(n)
            else:
                model_ids.add(dep_id)
        return model_ids, source_ids

    def collect_unselected_node_deps(
        self, selected_ids: t.Set[str]
    ) -> t.Tuple[t.Set[str], t.Set[str]]:
        """Collect unselected upstream dep IDs and source IDs for selected_ids."""
        dep_ids: t.Set[str] = set()
        source_ids: t.Set[str] = set()
        for node in self.iter_selected_nodes(selected_ids):
            model_node_ids, node_source_ids = self.resolve_deps(node)
            source_ids.update(node_source_ids)
            if selected_ids:
                dep_ids.update(model_node_ids - selected_ids)
        return dep_ids, source_ids

    @cached_property
    def state_deferred_fqn_by_unique_id(self) -> t.Dict[str, str]:
        return self.resolve_state_deferred_fqns()

    def resolve_state_deferred_fqns(self) -> t.Dict[str, str]:
        """Batch-resolve unselected upstream nodes to recorded prod FQNs.

        Returns an empty map when deferral is disabled, the dev target already
        is the defer-to profile, there are no deferred nodes, or the RPC fails
        for any reason.
        """
        if not self.defer_enabled or self._profiles.is_defer_to_profile:
            return {}
        dep_ids, _ = self.collect_unselected_node_deps(self.selected_resource_ids)
        if not dep_ids:
            return {}

        try:
            if not self._run_cache_config.dbt_project_id:
                events.fire_warn_event(
                    "State-based deferral could not use dbt project_id; falling back to project_name "
                    "for deferred relation lookup. Deferral will continue, but project_name fallback "
                    "is less precise if multiple projects in the organization share the same profile "
                    "and target. project_id can be specified in your dbt_project.yml"
                )
            request = execution_service_models.ResolveDeferredRelationsRequest(
                profile_name=self._config.profile_name,
                target_name=self._run_cache_config.defer_to,
                project_name=self._config.project_name,
                project_id=self._run_cache_config.dbt_project_id,
                node_unique_ids=sorted(dep_ids),
            )
            return self._query_cache_client.resolve_deferred_relations(request)
        except Exception as e:
            events.fire_debug_event("State deferral resolve failed: {}", str(e))
            return {}

    def state_deferred_table_parts(
        self, node: ManifestNode
    ) -> t.Optional[t.Tuple[t.Optional[str], t.Optional[str], str]]:
        """Return state-resolved table overrides for a deferred node, if available.

        Looks up the recorded prod FQN for node.unique_id and parses it into
        (database, schema, identifier). Returns None when there is no state
        entry for the node or when the FQN cannot be parsed, so callers can fall
        back to the macro-based deferred relation resolver.
        """
        state_fqn = self.state_deferred_fqn_by_unique_id.get(node.unique_id)
        if state_fqn is None:
            return None

        try:
            parsed = exp.to_table(state_fqn, dialect=self.dialect)
        except SqlglotError as e:
            events.fire_debug_event(
                "Failed to parse state-resolved deferred FQN '{}' for node {}: {}",
                state_fqn,
                node.unique_id,
                str(e),
            )
            return None

        if not parsed.name:
            events.fire_debug_event(
                "State-resolved deferred FQN '{}' for node {} did not contain a table name",
                state_fqn,
                node.unique_id,
            )
            return None

        return (
            parsed.catalog if parsed.catalog else None,
            parsed.db if parsed.db else None,
            parsed.name,
        )

    def node_to_deferred_table(self, node: ManifestNode) -> exp.Table:
        if (state_deferred_table_parts := self.state_deferred_table_parts(node)) is not None:
            database, schema, identifier = state_deferred_table_parts
            return self._adapter_ext._node_to_table(  # noqa: SLF001
                node,
                override_database=database,
                override_schema=schema,
                override_identifier=identifier,
            )

        assert self._deferred_relation_resolver is not None

        database = self._deferred_relation_resolver.get_deferred_database(node) or node.database
        schema = self._deferred_relation_resolver.get_deferred_schema(node) or node.schema
        identifier = self._deferred_relation_resolver.get_deferred_identifier(node) or node.alias

        return self._adapter_ext._node_to_table(  # noqa: SLF001
            node, override_database=database, override_schema=schema, override_identifier=identifier
        )

    @cached_property
    def selected_target_fqns(self) -> t.Set[str]:
        """FQNs of the relations the selected models and snapshots write to, computed once.

        This includes all --select'ed nodes, not just edges
        """
        return {
            self.node_to_table(node).sql(dialect=self.dialect)
            for node in self.iter_selected_nodes(self.selected_resource_ids)
        }

    @cached_property
    def dependency_kinds_by_fqn(self) -> t.Dict[str, shared_models.DependencyKind]:
        """Map table names to SOURCE, SEED, or MODEL, cached for this run.

        Include both local and deferred table names for upstream dependencies.
        Names shared by different kinds map to UNKNOWN; callers also use UNKNOWN
        for names absent from the manifest.
        """
        kinds: t.Dict[str, shared_models.DependencyKind] = {}
        deferred_ids, _ = (
            self.collect_unselected_node_deps(self.selected_resource_ids)
            if self.defer_enabled
            else (set(), set())
        )

        def add(table: exp.Table, kind: shared_models.DependencyKind) -> None:
            fqn = table.sql(dialect=self.dialect)
            previous = kinds.get(fqn)
            kinds[fqn] = (
                kind
                if previous is None or previous == kind
                else shared_models.DependencyKind.UNKNOWN
            )

        for source in self._manifest.sources.values():
            add(self.node_to_table(source), shared_models.DependencyKind.SOURCE)

        for node in self._manifest.nodes.values():
            if isinstance(node, SeedNode):
                kind = shared_models.DependencyKind.SEED
            elif isinstance(node, (ModelNode, SnapshotNode)):
                if isinstance(node, ModelNode) and node.get_materialization() == "ephemeral":
                    continue
                kind = shared_models.DependencyKind.MODEL
            else:
                continue

            add(self.node_to_table(node), kind)
            if node.unique_id in deferred_ids:
                add(self.node_to_deferred_table(node), kind)

        return kinds

    def get_defer_relation(self, node: ManifestNode) -> t.Optional[DeferRelation]:
        """Returns a DeferRelation for the given node if it should be deferred.

        A node is deferred when:
        - Deferral is enabled and the target is not already the defer-to profile
        - The node is not ephemeral
        - The node is not in the selected resource set

        Args:
            node: The manifest node to potentially defer.

        Returns:
            A DeferRelation if the node should be deferred, otherwise None.
        """
        if (
            not self.defer_enabled
            or self._profiles.is_defer_to_profile
            or getattr(node, "is_ephemeral", False)
            or node.unique_id in self.selected_resource_ids
        ):
            return None

        assert self._deferred_relation_resolver is not None
        compiled_code = getattr(node, "compiled_code", None)
        dev_relation = self._adapter_ext.adapter.Relation.create_from(self._config, node)  # type: ignore[arg-type]
        target_relation = self._defer_relation(dev_relation, node)
        target_relation_name = target_relation.render()

        defer_rel_kwargs: t.Dict[str, t.Any] = dict(
            database=target_relation.database or node.database,
            schema=target_relation.schema or node.schema,
            alias=target_relation.identifier or node.alias,
            relation_name=target_relation_name,
        )
        if DBT_VERSION >= (1, 8, 0):
            defer_rel_kwargs.update(
                dict(
                    resource_type=node.resource_type,
                    name=node.name,
                    description=node.description,
                    compiled_code=str(compiled_code) if compiled_code is not None else None,
                    meta=node.meta,
                    tags=node.tags,
                    config=node.config,
                )
            )
        defer_rel = DeferRelation(**defer_rel_kwargs)
        if self._run_cache_config.defer_logging_enabled:
            events.fire_event(
                self._run_cache_config.defer_log_level,
                "Deferring relation {} to {}",
                dev_relation.render(),
                target_relation_name,
            )
        return defer_rel

    def _defer_relation(self, relation: BaseRelation, target_node: ManifestNode) -> BaseRelation:
        deferred_relation = replace(relation, path=replace(relation.path))

        if (state_deferred_table_parts := self.state_deferred_table_parts(target_node)) is not None:
            database, schema, identifier = state_deferred_table_parts
            deferred_relation.path.database = database
            deferred_relation.path.schema = schema
            deferred_relation.path.identifier = identifier
            return deferred_relation

        assert self._deferred_relation_resolver is not None

        deferred_relation.path.schema = self._deferred_relation_resolver.get_deferred_schema(
            target_node
        )
        deferred_relation.path.database = self._deferred_relation_resolver.get_deferred_database(
            target_node
        )
        deferred_relation.path.identifier = (
            self._deferred_relation_resolver.get_deferred_identifier(target_node)
        )
        return deferred_relation
