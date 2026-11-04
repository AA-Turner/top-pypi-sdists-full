from __future__ import annotations

import json
import typing as t
from datetime import datetime
from time import perf_counter

from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.nodes import GenericTestNode, ModelNode, SeedNode, SingularTestNode
from query_cache_common.constants import SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
from query_cache_common.models import shared_models
from query_cache_common.models.services import clone_service_models, sql_service_models
from query_cache_common.models.services.clone_service_models import TableProperties
from sqlglot import exp

from dbt_state import events
from dbt_state.adapters import BaseAdapterExtension
from dbt_state.adapters.common import ViewTraversalResult
from dbt_state.config import RunCacheConfig
from dbt_state.freshness import Freshness
from dbt_state.node_hash_calculator import ModelNodeHashCalculator, create_node_hash_calculator
from dbt_state.node_resolution import NodeResolution
from dbt_state.prefetch import MetadataPrefetcher
from dbt_state.profiles import Profiles
from dbt_state.utils import (
    is_custom_materialization,
    is_full_refresh,
    is_incremental_or_snapshot,
    is_view,
)

if t.TYPE_CHECKING:
    from dbt_state._typing import (
        ModelOrSnapshotOrTestNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )

# Semantic-extras keys used to fold a microbatch model run's whole resolved event-time
# window into the model-level cache key, so the run's outcome is keyed to the window it
# was computed for.
MICROBATCH_EVENT_TIME_START_KEY = "__microbatch_event_time_start"
MICROBATCH_EVENT_TIME_END_KEY = "__microbatch_event_time_end"

# Semantic-extras key used to fold the hash of a node's persisted documentation (relation
# and/or column descriptions, when persist_docs is enabled) into the cache key. This ensures
# that a docs-only change triggers an execution so the new descriptions are written to the
# target table, even when the query result is otherwise unchanged.
PERSISTED_DOCS_HASH_KEY = "__persisted_docs_hash"


# Additional model configs that impact data outcomes and should be included in hash calculations
SEMANTIC_EXTRAS_CONFIG_KEYS = (
    "on_schema_change",
    "incremental_predicates",
    "merge_update_columns",
    "merge_exclude_columns",
    "contract",
    "constraints",
    "cluster_by",
    "unique_key",
    "grants",
    "event_time",
    "sql_header",
    "lookback",
    "partition_by",
    "table_format",
    # Test attributes
    "severity",
    "limit",
    "where",
    "fail_calc",
    "warn_if",
    "error_if",
    "store_failures",
    "store_failures_as",
    # Databricks attributes
    "auto_liquid_cluster",
    "databricks_tags",
    "file_format",
    "location_root",
    "include_full_name_in_path",
    "clustered_by",
    "buckets",
    "liquid_clustered_by",
    "tblproperties",
    # Snowflake attributes
    "transient",
    "target_lag",
    "refresh_mode",
    "immutable_where",
    "copy_grants",
    "tmp_relation_type",
    # Postgres attributes
    "unlogged",
    "indexes",
    # Bigquery attributes
    "require_partition_filter",
    "partition_expiration_days",
    "hours_to_expiration",
    # Redshift attributes
    "dist",
    "sort",
    "sort_type",
)


def _serialize_semantic_extra(key: str, value: t.Any) -> str:
    if value is None:
        return ""

    normalized_value = value.to_dict() if hasattr(value, "to_dict") else value
    try:
        return json.dumps(normalized_value, sort_keys=True)
    except TypeError as e:
        raise TypeError(f"Failed to serialize semantic extra {key}:", str(e)) from e


# Model configs that affect a view's outcome without changing its SQL. Views use a
# narrower set than SEMANTIC_EXTRAS_CONFIG_KEYS since most table configs don't apply.
VIEW_SEMANTIC_EXTRAS_CONFIG_KEYS = ("grants",)

SEED_SEMANTIC_EXTRAS_CONFIG_KEYS = (
    "column_types",
    "quote_columns",
    "delimiter",
)


class RequestBuilder:
    """Builds the SQL, values and clone requests sent to the query cache for a dbt node.

    Owns the clone time travel limit and derives the clone chain depth limit and table namespace
    that scope cache decisions.
    """

    def __init__(
        self,
        adapter_ext: BaseAdapterExtension,
        node_resolution: NodeResolution,
        freshness: Freshness,
        prefetcher: MetadataPrefetcher,
        profiles: Profiles,
        manifest: Manifest,
        config: RuntimeConfig,
        run_cache_config: RunCacheConfig,
    ) -> None:
        self._adapter_ext = adapter_ext
        self._node_resolution = node_resolution
        self._freshness = freshness
        self._prefetcher = prefetcher
        self._profiles = profiles
        self._manifest = manifest
        self._config = config
        self._run_cache_config = run_cache_config
        self._clone_time_travel_limit: t.Optional[int] = (
            run_cache_config.clone_time_travel_limit
            if adapter_ext.adapter.type() in SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
            else 0
        )

    @staticmethod
    def validate_positive_int(value: t.Any, field_name: str) -> t.Optional[int]:
        if value is None:
            return None
        value = int(value)
        if value <= 0:
            events.fire_warn_event("Invalid {}={} (must be > 0), ignoring", field_name, value)
            return None
        return value

    def get_table_properties(
        self, node: ModelOrSnapshotOrTestOrSeedNode
    ) -> t.Optional[TableProperties]:
        hours = self.validate_positive_int(
            node.config.extra.get("hours_to_expiration"), "hours_to_expiration"
        )
        partition_days = self.validate_positive_int(
            node.config.extra.get("partition_expiration_days"),
            "partition_expiration_days",
        )
        if hours is None and partition_days is None:
            return None
        return TableProperties(
            hours_to_expiration=hours,
            partition_expiration_days=partition_days,
        )

    def build_submit_values_request(
        self,
        node: SeedNode,
    ) -> sql_service_models.SubmitValuesRequest:
        node_config = node.config
        semantic_extras = {
            key: _serialize_semantic_extra(key, node_config.get(key))
            for key in SEED_SEMANTIC_EXTRAS_CONFIG_KEYS
            if key in node_config
        }
        semantic_extras.update(self.persisted_docs_semantic_extras(node))
        last_modified_epoch = self._freshness.get_last_modified_epoch(
            self._node_resolution.node_to_table(node)
        )

        calculator = create_node_hash_calculator(node, self._manifest, self._config)

        dbt_node_state = shared_models.DbtNodeState(
            node_unique_id=node.unique_id,
            target_name=self._config.target_name,
            project_name=self._config.project_name,
            resource_type=node.resource_type,
            node_hash=calculator.calculate_node_hash(),
            node_body_hash=calculator.node_body_hash,
            node_configs_hash=calculator.node_configs_hash,
            node_persisted_descriptions_hash=calculator.node_persisted_docs_hash,
            node_macros_hash=calculator.node_macros_hash,
            node_contract_hash=None,
            profile_name=self._config.profile_name,
            project_id=self._run_cache_config.dbt_project_id,
        )

        return sql_service_models.SubmitValuesRequest(
            target_table=node.relation_name or "",
            dialect=self._node_resolution.dialect,
            default_catalog=self._adapter_ext.default_catalog,
            values_hash=calculator.calculate_node_hash(),
            semantic_extras=semantic_extras,
            last_modified_epoch=last_modified_epoch,
            labels=self.get_request_labels(node),
            clone_time_travel_limit=self._clone_time_travel_limit,
            clone_table_properties=self.get_table_properties(node),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
            dbt_node_state=dbt_node_state,
            table_namespace=self.table_namespace,
            allow_clones=self._run_cache_config.allow_clones,
            is_defer_to_profile=self._profiles.is_defer_to_profile,
            defer_enabled=self._node_resolution.defer_enabled,
        )

    def build_submit_enriched_sql_request(
        self,
        node: ModelOrSnapshotOrTestNode,
        sql: str,
        execution_type: shared_models.ModelExecutionType,
        traversal_result: t.Optional[ViewTraversalResult],
        microbatch_window: t.Optional[t.Tuple[datetime, datetime]] = None,
        speculative: bool = False,
    ) -> t.Tuple[sql_service_models.SubmitEnrichedSQLRequest, int]:
        target_table = (
            self._node_resolution.node_to_table(node).sql(dialect=self._node_resolution.dialect)
            if execution_type != shared_models.ModelExecutionType.DBT_DATA_TEST
            else None
        )
        dialect = self._node_resolution.dialect
        default_catalog = self._adapter_ext.default_catalog
        node_config = node.config

        if execution_type == shared_models.ModelExecutionType.VIEW:
            # Views don't need dependency traversal — only the view's own last_modified_epoch
            # and query hash matter, since the query is re-evaluated every time the view is queried
            assert target_table is not None
            last_modified_start = perf_counter()
            last_modified_epoch = (
                self._adapter_ext.get_available_last_modified_epochs([target_table])
                if speculative
                else self._adapter_ext.get_last_modified_epoch([target_table])
            )
            last_modified_duration_ms = int((perf_counter() - last_modified_start) * 1000)
            table_infos = [
                shared_models.TableModifiedInfo(name=name, last_modified_epoch=epoch)  # ty: ignore[invalid-argument-type]
                for name, epoch in last_modified_epoch.items()
            ]
            semantic_extras = {
                key: _serialize_semantic_extra(key, node_config.get(key))
                for key in VIEW_SEMANTIC_EXTRAS_CONFIG_KEYS
                # Skip empty values (e.g. dbt's default grants={}) so views that don't set
                # these configs keep the same hash as before they were added here.
                if key in node_config and node_config.get(key)
            }
            semantic_extras.update(self.persisted_docs_semantic_extras(node))
            return sql_service_models.SubmitEnrichedSQLRequest(
                tables=table_infos,
                query_dependencies=[],
                target_table=target_table,
                dialect=dialect,
                default_catalog=default_catalog,
                default_schema=self._adapter_ext.DEFAULT_SCHEMA_NAME,
                execution_type=execution_type,
                sql=sql,
                semantic_extras=semantic_extras,
                freshness_tolerance_seconds=0,
                tolerate_nondeterminism=True,
                labels=self.get_request_labels(node),
                clone_time_travel_limit=self._clone_time_travel_limit,
                clone_table_properties=self.get_table_properties(node),
                stale_upstream_policy=self._run_cache_config.resolve_stale_upstream_policy(
                    node_config
                ),
                clone_chain_depth_limit=self.clone_chain_depth_limit,
                dbt_node_state=self.build_dbt_node_state(node),
                compare_unrendered_code=self._run_cache_config.resolve_compare_unrendered_code(
                    node_config
                ),
                table_namespace=self.table_namespace,
                ignore_external_modifications=self._run_cache_config.resolve_ignore_external_modifications(
                    node_config
                ),
                allow_clones=self._run_cache_config.allow_clones,
                is_defer_to_profile=self._profiles.is_defer_to_profile,
                defer_enabled=self._node_resolution.defer_enabled,
            ), last_modified_duration_ms

        # The caller owns the view traversal so the speculative decision can be made after it
        # completes (see _submit_sql_request); it must be supplied for non-view execution types.
        if traversal_result is None:
            raise RuntimeError("Traversal result is required for non-view nodes")

        # Include the target table's last modified epoch to enable detection of unobserved modifications
        all_tables = traversal_result.seen_tables.copy()
        if target_table is not None:
            all_tables.add(target_table)
        last_modified_start = perf_counter()

        if speculative:
            last_modified_epoch = self._adapter_ext.get_available_last_modified_epochs(all_tables)
            # Views whose definition could not be resolved have no reliable freshness signal.
            # Force them unset (treated as "now" server-side) even if a stale epoch happens to be
            # cached, so a speculative decision cannot treat them as fresh — matching the
            # non-speculative path, which overrides them to "now".
            for fqn in traversal_result.unresolvable_tables:
                if fqn in last_modified_epoch:
                    last_modified_epoch[fqn] = None
        else:
            overrides = {}
            source_freshness_overrides = (
                self._freshness.resolve_dbt_source_freshness_overrides(node)
                if isinstance(node, ModelNode)
                else {}
            )
            overrides.update(source_freshness_overrides)

            unresolvable = traversal_result.unresolvable_tables
            if unresolvable:
                self._adapter_ext.clear_last_modified_cache(unresolvable)
                now_ms = self._freshness.get_heuristic_now_epoch()
                if now_ms:
                    unresolvable_without_override = [
                        fqn for fqn in unresolvable if fqn not in overrides
                    ]
                    if unresolvable_without_override:
                        events.fire_warn_event(
                            "Could not determine freshness for {}; treating as modified."
                            " Configure loaded_at_field or loaded_at_query to set freshness timestamp.",
                            ", ".join(unresolvable_without_override),
                        )
                    overrides.update(
                        {fqn: (lambda v=now_ms: v) for fqn in unresolvable_without_override}
                    )

            last_modified_epoch = self._adapter_ext.get_last_modified_epoch(
                all_tables, table_overrides=overrides
            )

        last_modified_duration_ms = int((perf_counter() - last_modified_start) * 1000)

        # Only edge table schemas are fetched, so we intentionally exclude them from TableModifiedInfo
        # entries to avoid the sparseness problem where most tables will not have any schemas set.
        # Speculative requests omit schemas entirely: impact analysis is not applied to them, so
        # blocking on the schema prefetch here would defeat the point of speculating.
        table_schemas: t.List[shared_models.TableSchema] = []
        compare_selected_columns = self._run_cache_config.resolve_compare_selected_columns(
            node_config
        )
        if compare_selected_columns and not speculative:
            # traversal_result.seen_tables contains the all the upstream tables that this model
            # depends on, plus the ones that are only reachable through view definitions
            # we remove the ones that have already been handled by this run, because those
            # already have schemas stored in state that the server can use
            edge_tables = traversal_result.seen_tables - self._node_resolution.selected_target_fqns

            if target_table is not None:
                edge_tables.discard(target_table)

            if edge_tables:
                self._prefetcher.await_prefetch_schemas()
                table_schemas = [
                    shared_models.TableSchema(
                        name=name,
                        columns=[
                            shared_models.ColumnInfo(name=column, type=data_type)
                            for column, data_type in columns.items()
                        ],
                    )
                    for name, columns in self._adapter_ext.get_schemas(edge_tables).items()
                    if columns is not None
                ]

        dependency_kinds = (
            self._node_resolution.dependency_kinds_by_fqn if compare_selected_columns else {}
        )
        table_infos = [
            shared_models.TableModifiedInfo(
                name=name,
                last_modified_epoch=epoch,  # ty: ignore[invalid-argument-type]
                kind=dependency_kinds.get(name, shared_models.DependencyKind.UNKNOWN),
            )
            for name, epoch in last_modified_epoch.items()
        ]
        query_dependencies = [
            shared_models.QueryDependency(
                name=name,
                query=v.definition,
                default_catalog=v.default_catalog,
                default_schema=v.default_schema,
            )
            for name, v in traversal_result.view_definitions.items()
        ]

        semantic_extras = {
            key: _serialize_semantic_extra(key, node_config.get(key))
            for key in SEMANTIC_EXTRAS_CONFIG_KEYS
            if key in node_config
        }
        if microbatch_window is not None:
            # microbatch_window is only ever passed for microbatch models (see
            # microbatch_execute_override), including under --full-refresh, so its
            # presence already scopes this injection correctly without checking
            # execution_type.
            start, end = microbatch_window
            semantic_extras[MICROBATCH_EVENT_TIME_START_KEY] = start.isoformat()
            semantic_extras[MICROBATCH_EVENT_TIME_END_KEY] = end.isoformat()

        semantic_extras.update(self.persisted_docs_semantic_extras(node))
        return sql_service_models.SubmitEnrichedSQLRequest(
            tables=table_infos,
            query_dependencies=query_dependencies,
            target_table=target_table,
            dialect=dialect,
            default_catalog=default_catalog,
            default_schema=self._adapter_ext.DEFAULT_SCHEMA_NAME,
            execution_type=execution_type,
            sql=sql,
            semantic_extras=semantic_extras,
            freshness_tolerance_seconds=self._run_cache_config.resolve_freshness_tolerance(
                node_config
            ),
            tolerate_nondeterminism=self._run_cache_config.resolve_tolerate_nondeterminism(
                node_config
            ),
            labels=self.get_request_labels(node),
            clone_time_travel_limit=self._clone_time_travel_limit,
            clone_table_properties=self.get_table_properties(node),
            stale_upstream_policy=self._run_cache_config.resolve_stale_upstream_policy(node_config),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
            dbt_node_state=self.build_dbt_node_state(node),
            compare_unrendered_code=self._run_cache_config.resolve_compare_unrendered_code(
                node_config
            ),
            table_namespace=self.table_namespace,
            ignore_external_modifications=self._run_cache_config.resolve_ignore_external_modifications(
                node_config
            ),
            allow_clones=self._run_cache_config.allow_clones,
            is_defer_to_profile=self._profiles.is_defer_to_profile,
            defer_enabled=self._node_resolution.defer_enabled,
            table_schemas=table_schemas,
            compare_selected_columns=compare_selected_columns,
        ), last_modified_duration_ms

    def build_clone_request(
        self,
        node: ModelOrSnapshotOrTestNode,
        clone_source: str,
        clone_source_table_type: t.Optional[str],
    ) -> clone_service_models.CloneRequest:
        clone_source_last_modified_epoch = self._freshness.get_last_modified_epoch(
            exp.to_table(clone_source, dialect=self._node_resolution.dialect)
        )
        return clone_service_models.CloneRequest(
            target_table=node.relation_name or "",
            clone_source_table=clone_source,
            dialect=self._node_resolution.dialect,
            default_catalog=self._adapter_ext.default_catalog,
            execution_type=shared_models.ModelExecutionType(self.node_execution_type(node)),
            clone_source_last_modified_epoch=clone_source_last_modified_epoch,
            labels=self.get_request_labels(node),
            clone_source_table_type=clone_source_table_type,
            table_properties=self.get_table_properties(node),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
            table_namespace=self.table_namespace,
        )

    @staticmethod
    def get_request_labels(node: ModelOrSnapshotOrTestOrSeedNode) -> t.Dict[str, str]:
        unique_id = node.unique_id

        return {
            "dbt_node_name": node.name,
            "dbt_node_fqn": ".".join(node.fqn),
            "dbt_node_unique_id": unique_id,
        }

    def persisted_docs_semantic_extras(
        self, node: ModelOrSnapshotOrTestOrSeedNode
    ) -> t.Dict[str, str]:
        """Build the persisted-docs semantic extra for a node.

        When ``persist_docs`` is enabled for a node, its relation and/or column descriptions
        are written to the target table. A change to those descriptions does not alter the
        query result, so without this extra the cache would report a no-op and the updated
        docs would never be persisted. Folding the docs hash into ``semantic_extras`` forces
        an execution whenever the documentation changes. Returns an empty mapping when the
        node has no persisted docs.
        """
        calculator = create_node_hash_calculator(node, self._manifest, self._config)
        docs_hash = calculator.node_persisted_docs_hash
        if docs_hash is None:
            return {}
        return {PERSISTED_DOCS_HASH_KEY: docs_hash}

    def build_dbt_node_state(self, node: ModelOrSnapshotOrTestNode) -> shared_models.DbtNodeState:
        calculator = create_node_hash_calculator(
            node,
            self._manifest,
            self._config,
            include_runtime_vars=self._run_cache_config.resolve_compare_unrendered_code(
                node.config
            ),
        )

        node_contract_hash: t.Optional[str] = None
        if isinstance(calculator, ModelNodeHashCalculator):
            node_contract_hash = calculator.node_contract_hash

        return shared_models.DbtNodeState(
            node_unique_id=node.unique_id,
            target_name=self._config.target_name,
            project_name=self._config.project_name,
            resource_type=node.resource_type,
            node_hash=calculator.calculate_node_hash(),
            node_body_hash=calculator.node_body_hash,
            node_configs_hash=calculator.node_configs_hash,
            node_persisted_descriptions_hash=calculator.node_persisted_docs_hash,
            node_macros_hash=calculator.node_macros_hash,
            node_contract_hash=node_contract_hash,
            profile_name=self._config.profile_name,
            project_id=self._run_cache_config.dbt_project_id,
            node_database_representation=(
                f"{node.database}.{node.schema}.{node.alias}"
                if node.database and node.schema and node.alias
                else None
            ),
        )

    def node_execution_type(self, node: ModelOrSnapshotOrTestNode) -> str:
        if isinstance(node, (GenericTestNode, SingularTestNode)):
            return "DBT_DATA_TEST"
        if is_view(node):
            return "VIEW"
        if is_custom_materialization(node):
            return "DBT_CUSTOM"
        execution_type = "full"
        if is_incremental_or_snapshot(node) and not is_full_refresh(self._config, node):
            if node.resource_type == "snapshot":
                execution_type = "snapshot"
            else:
                execution_type_str = getattr(node.config, "incremental_strategy", None) or "append"
                execution_type = execution_type_str.replace("+", "_").lower()
                if execution_type == "merge" and not getattr(node.config, "unique_key", None):
                    execution_type = "append"
        return execution_type.upper()

    @property
    def clone_chain_depth_limit(self) -> t.Optional[int]:
        # if cloning is disabled by config; send clone_chain_depth_limit=0 to exclude clone candidates
        if not self._run_cache_config.allow_clones:
            return 0

        default_limit = self._adapter_ext.CLONE_CHAIN_DEPTH_LIMIT

        # in prod, we set 1 less than the actual limit (which may force an execute instead of a clone)
        # this ensures that there is always at least 1 more clone left for a dev clone
        if (
            self._node_resolution.defer_enabled
            and self._profiles.is_defer_to_profile
            and default_limit is not None
        ):
            return max(default_limit - 1, 0)

        return default_limit

    @property
    def table_namespace(self) -> str:
        """An identifier to tag a group of tables with. Cache decisions are then scoped to tables tagged with the same namespace.

        This prevents for example a "skip" response being returned based on an execution record that was actually executed
        against a different database server and table in question doesn't even exist in the current database server.

        A common place this can occur is in CI pipelines, where CI executes against an isolated fresh/empty database that is specified
        using an environment variable (and nothing else about the project is changed - identical catalog, default schema, table names etc).

        Without namespaces, the state server could return Skip or Clone decisions based on the production database, not the CI one
        """
        # this is adapter-specific but essentially tries to tag a unique connection
        # for example, the Snowflake adapter includes the snowflake account_id and the Postgres adapter includes the database hostname
        return self._config.credentials.hashed_unique_field()
