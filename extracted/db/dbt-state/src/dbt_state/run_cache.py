from __future__ import annotations

import sys
import threading
import typing as t
import json
import uuid
from concurrent.futures import Future
from dataclasses import dataclass, replace
from datetime import datetime
from functools import cached_property
from time import perf_counter

import agate
import grpc
import humanize

from sqlglot import exp, parse_one
from sqlglot.errors import SqlglotError

from dbt.adapters.base.relation import BaseRelation, RelationType

try:
    from dbt.adapters.contracts.connection import AdapterResponse
    from dbt.artifacts.resources.v1.components import DeferRelation
except ImportError:
    from dbt.contracts.connection import AdapterResponse  # type: ignore
    from dbt.contracts.graph.nodes import DeferRelation  # type: ignore[no-redef]

from dbt.clients.jinja import get_rendered
from dbt.config.runtime import RuntimeConfig
from dbt.contracts.results import RunResult, RunStatus
from dbt.context.providers import generate_runtime_model_context, RuntimeProvider
from dbt.contracts.graph.manifest import Manifest, SourceDefinition
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ModelNode,
    ManifestNode,
    ManifestSQLNode,
    SeedNode,
    SnapshotNode,
    SingularTestNode,
)

try:
    from dbt_common.clients import agate_helper
except ImportError:
    from dbt.clients import agate_helper  # type: ignore

from dbt_state import events
from dbt_state.adapters import create_adapter_extension, BaseAdapterExtension
from dbt_state.adapters.common import ViewTraversalResult
from dbt_state.adapters.clock import EngineHeuristicsClock
from dbt_state.config import RunCacheConfig
from dbt_state.dev_cloner import DevCloner
from dbt_state.dispatcher import TelemetryDispatcher
from dbt_state.session import SessionManager
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.profiles import Profiles
from dbt_state.relation import DeferredRelationResolver
from dbt_state.utils import (
    get_dbt_command_name,
    is_custom_materialization,
    is_full_refresh,
    is_incremental_or_snapshot,
    is_table,
    is_view,
    DBT_VERSION,
)
from dbt_state.decision_logger import create_decision_logger, BaseDecisionLogger
from dbt_state.node_hash_calculator import (
    ModelNodeHashCalculator,
    create_node_hash_calculator,
)
from query_cache_common.constants import NO_OP_STATUS, SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
from query_cache_common.models import shared_models
from query_cache_common.models.services import (
    client_telemetry_service_models,
    sql_service_models,
    clone_service_models,
    execution_service_models,
)
from query_cache_common.models.services.explain_service_models import ExplainMessageEntry
from query_cache_common.models.services.clone_service_models import TableProperties

# Feature-detect RunStatus.Reused. dbt-core added this member in
# https://github.com/dbt-labs/dbt-core/pull/12912 (target: 1.11.0); older clients
# only support Success/Error/Skipped/PartialSuccess/NoOp.
_RUN_STATUS_REUSED = getattr(RunStatus, "Reused", None)

if t.TYPE_CHECKING:
    from dbt.adapters.base import BaseRelation
    from dbt.adapters.sql import SQLAdapter
    from dbt.artifacts.resources.v1.config import TestConfig
    from dbt.artifacts.resources.v1.model import ModelConfig
    from dbt.artifacts.resources.v1.snapshot import SnapshotConfig
    from dbt_state._typing import (
        ModelOrSnapshotNode,
        ModelOrSnapshotOrSeedNode,
        ModelOrSnapshotOrTestNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )

RequestId = str
FailedToClone = bool

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
        raise TypeError(f"Failed to serialize semantic extra {key}:", str(e))


SEED_SEMANTIC_EXTRAS_CONFIG_KEYS = (
    "column_types",
    "quote_columns",
    "delimiter",
)

_HASH_READ_CHUNK_SIZE = 64 * 1024


@dataclass
class NoRunResult:
    request_id: str
    """The unique identifier for the execution request."""
    failed_to_clone: bool


@dataclass
class CacheBypassedResponse:
    """A local "response" that defers recording the execution outcome until after the node runs.

    Returned when the cache is in write-only mode, and also for a speculative
    untracked-execute verdict in read-write mode, in both cases containing the request that
    should be sent once the node has executed.

    When ``speculative`` is set, the request was built from partial (still-prefetching)
    dependency timestamps, so its timestamps must be finalized against the completed
    prefetch before the outcome is recorded.
    """

    request: t.Union[
        sql_service_models.SubmitEnrichedSQLRequest, sql_service_models.SubmitValuesRequest
    ]
    node: ModelOrSnapshotOrTestOrSeedNode
    speculative: bool = False


class RunCache:
    def __init__(
        self,
        query_cache_client: QueryCacheGrpcClient,
        dev_cloner: t.Optional[DevCloner],
        profiles: Profiles,
        deferred_relation_resolver: t.Optional[DeferredRelationResolver],
        adapter_ext: BaseAdapterExtension,
        config: RuntimeConfig,
        manifest: Manifest,
        decision_logger: BaseDecisionLogger,
        run_cache_config: RunCacheConfig,
        telemetry_dispatcher: TelemetryDispatcher,
        session_manager: SessionManager,
    ) -> None:
        self._query_cache_client = query_cache_client
        self._dev_cloner = dev_cloner
        self._profiles = profiles
        self._deferred_relation_resolver = deferred_relation_resolver
        self._dev_cloned_nodes: t.Set[str] = set()
        self._deferred_fqns: t.Set[str] = set()
        self._adapter_ext = adapter_ext
        self._config = config
        self._manifest = manifest
        self._decision_logger = decision_logger
        self._run_cache_config = run_cache_config
        self._telemetry_dispatcher = telemetry_dispatcher
        self._session_manager = session_manager

        self._engine_heuristics_clock = EngineHeuristicsClock(adapter_ext)
        self._engine_heuristics_clock_disabled = False
        self._use_heuristic_clock_for_last_modified: bool = (
            adapter_ext.use_heuristic_clock_for_last_modified
        )

        self._prefetch_tables_lock = threading.Lock()
        self._prefetch_started: bool = False
        self._prefetch_future: t.Optional[Future[None]] = None
        self._prefetch_done: bool = False

        self._total_cache_hits: int = 0
        self._total_time_saved_ms: int = 0
        self._reused_status_warning_emitted: bool = False
        events.register_callback("run-cache", self.on_event)

        self._run_result = client_telemetry_service_models.ClientResult.SUCCESS

        self._clone_time_travel_limit: t.Optional[int] = (
            run_cache_config.clone_time_travel_limit
            if self.dialect in SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
            else 0
        )

        # map of node.unique_id -> CacheBypassedResponse
        # collected in _process_query_cache_response and published as write-only executions
        self._cache_bypass_responses: t.Dict[str, CacheBypassedResponse] = {}

    @classmethod
    def create(
        cls,
        run_cache_config: RunCacheConfig,
        config: RuntimeConfig,
        adapter: SQLAdapter,
        manifest: Manifest,
        query_cache_client: QueryCacheGrpcClient,
        telemetry_dispatcher: TelemetryDispatcher,
        session_manager: SessionManager,
        decision_logger: t.Optional[BaseDecisionLogger] = None,
    ) -> RunCache:
        profiles = Profiles.from_config(config, run_cache_config)
        adapter_ext = create_adapter_extension(
            adapter,
            threads=config.threads,
            cache_ttl_seconds=run_cache_config.metadata_cache_ttl,
            get_view_ddl_override=run_cache_config.snowflake_get_view_ddl_override,
            metadata_warehouse=run_cache_config.snowflake_metadata_warehouse,
        )
        if profiles.has_defer_to_profile:
            deferred_relation_resolver: t.Optional[DeferredRelationResolver] = (
                DeferredRelationResolver(
                    config=config,
                    manifest=manifest,
                    defer_to_profile=profiles.defer_to_profile,
                )
            )
            dev_cloner: t.Optional[DevCloner] = DevCloner(
                config=config,
                adapter_ext=adapter_ext,
                profiles=profiles,
                deferred_relation_resolver=deferred_relation_resolver,
                run_cache_config=run_cache_config,
            )
        else:
            events.fire_debug_event(
                "Target '{}' not found in profile '{}'. Deferral and dev cloning are disabled",
                run_cache_config.defer_to,
                config.profile_name,
            )
            deferred_relation_resolver = None
            dev_cloner = None
        if decision_logger is None:
            decision_logger = create_decision_logger(
                project_root=config.project_root,
                log_path=config.log_path,
                config=run_cache_config,
            )
            decision_logger.log_run_start(config)
        if (
            run_cache_config.clone_time_travel_limit is not None
            and run_cache_config.clone_time_travel_limit > 0
            and adapter.type() not in SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
        ):
            events.fire_warn_event(
                "clone_time_travel_limit is configured but %s does not support time travel for cloning. "
                "The setting will be ignored.",
                adapter.type(),
            )
        return cls(
            query_cache_client=query_cache_client,
            dev_cloner=dev_cloner,
            profiles=profiles,
            deferred_relation_resolver=deferred_relation_resolver,
            adapter_ext=adapter_ext,
            config=config,
            manifest=manifest,
            decision_logger=decision_logger,
            run_cache_config=run_cache_config,
            telemetry_dispatcher=telemetry_dispatcher,
            session_manager=session_manager,
        )

    def on_execute(
        self,
        node: t.Union[ModelOrSnapshotNode, SeedNode],
        *,
        microbatch_window: t.Optional[t.Tuple[datetime, datetime]] = None,
    ) -> RunResult | NoRunResult | None:
        """Invoked before executing a model node.

        Invokes the query cache to determine if the model execution can be skipped
        or replaced with a clone operation.

        Args:
            node: The model node being executed.
            microbatch_window: The resolved (start, end) event-time window for a microbatch
                model's whole run, if any. Folded into the request's semantic extras so
                the model-level cache key reflects the window being processed.

        Returns:
            One of the following:
            - A RunResult if the execution was skipped or replaced with a clone, otherwise None to proceed with normal execution.
            - A RequestId if the execution should proceed normally but needs to be confirmed once it's done.
            - None if the execution should proceed normally without confirmation.
        """
        if isinstance(node, SeedNode):
            query_cache_response = self._submit_values_request(node)
        elif (
            isinstance(node, (ModelNode, SnapshotNode))
            and node.language == "sql"
            and (
                is_table(node) or (is_view(node) and self._adapter_ext.supports_view_last_modified)
            )
        ):
            query_cache_response = self._submit_sql_request(
                node, microbatch_window=microbatch_window
            )
        else:
            return None
        return self._process_query_cache_response(node, query_cache_response)

    def on_compile(self, node: ManifestSQLNode) -> None:
        """Invoked during the compilation of a model node.

        Automatically clones selected incremental models when appropriate, except
        during dbt compile because compile must not create or mutate relations.

        Args:
            node: The model node being compiled.
        """
        try:
            self._start_prefetch_last_modified()
        except Exception as e:
            events.fire_warn_event("Failed to prefetch last modified timestamps: {}", str(e))

        if isinstance(node, (ModelNode, SnapshotNode)) and not self._is_dbt_compile_command:
            if self._try_clone(node):
                self._dev_cloned_nodes.add(node.unique_id)

    @cached_property
    def _is_dbt_compile_command(self) -> bool:
        """Whether the top-level dbt command is compile.

        dbt also invokes model compile hooks while running commands like run and build.
        Those commands can still clone; only dbt compile must avoid relation mutations.
        """
        return get_dbt_command_name(getattr(self._config, "args", None)) == "compile"

    def get_defer_relation(self, node: ManifestNode) -> t.Optional[DeferRelation]:
        """Returns a DeferRelation for the given node if it should be deferred.

        A node is deferred when:
        - Deferral is enabled and the target is not already the defer-to profile
        - The node is not ephemeral
        - The node is not in the selected resource set

        Also tracks the deferred relation name in ``_deferred_nodes`` for lenient
        dependency matching in cache requests.

        Args:
            node: The manifest node to potentially defer.

        Returns:
            A DeferRelation if the node should be deferred, otherwise None.
        """
        if (
            not self._defer_enabled
            or self._profiles.is_defer_to_profile
            or getattr(node, "is_ephemeral", False)
            or node.unique_id in self._selected_resource_ids
        ):
            return None

        assert self._deferred_relation_resolver is not None
        compiled_code = getattr(node, "compiled_code", None)
        dev_relation = self._adapter.Relation.create_from(self._config, node)  # type: ignore[arg-type]
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
        self._deferred_fqns.add(self._adapter_ext.relation_to_fqn(target_relation))
        return defer_rel

    def cache_compiled_view_sql(self, node: ManifestSQLNode) -> None:
        """Pre-populate the view definition cache from a compiled dbt model node.

        Only caches plain view models (not materialized_view, ephemeral, etc.) that have
        compiled SQL available. This avoids expensive database round-trips for views whose
        SQL is already known from dbt compilation.

        Args:
            node: The compiled manifest node to potentially cache.
        """
        if (
            isinstance(node, ModelNode)
            and (node.get_materialization() or "view") == "view"
            and node.compiled_code
        ):
            table = self._node_to_table(node)
            self._adapter_ext.cache_view_definition(
                table=table,
                definition=node.compiled_code,
                default_schema=node.schema,
            )

    def data_test_adapter_proxy(
        self, node: t.Union[GenericTestNode, SingularTestNode]
    ) -> _DataTestAdapterProxy:
        """Returns a proxy adapter for executing SQL related to data tests that checks the query cache before executing the test SQL.

        Args:
            node: The test node being executed.

         Returns:
            A proxy adapter that can be used to execute data test SQL with query cache integration.
        """
        return _DataTestAdapterProxy(node, self)

    def on_event(self, msg: events.EventMsg) -> None:
        if msg.info.name == "ResourceReport":
            if hasattr(msg.data, "command_success") and isinstance(msg.data.command_success, bool):
                if msg.data.command_success:
                    self._run_result = client_telemetry_service_models.ClientResult.SUCCESS
                else:
                    self._run_result = client_telemetry_service_models.ClientResult.FAILURE
        elif msg.info.name == "CommandCompleted":
            self._session_manager.end(
                result=self._run_result, description="", metrics=self._adapter_ext.report()
            )

    def confirm_execution(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        request_id: RequestId,
        failed_to_clone: bool = False,
        execution_runtime_ms: t.Optional[int] = None,
    ) -> None:
        """Confirms the execution of a model node with the query cache service.

        Args:
            node: The model node that was executed.
            request_id: The request ID returned from the query cache for the given model's execution.
            failed_to_clone: Whether the model failed to be cloned during execution.
        """
        target_table_type, last_modified_epoch = (
            self._get_target_table_type_and_last_modified_epoch(node)
        )
        if last_modified_epoch is None:
            events.fire_debug_event(
                "Skipping confirmation for node {} due to missing last modified epoch",
                node.unique_id,
            )
            return

        confirmation_request = execution_service_models.ConfirmExecutionRequest(
            request_id=request_id,
            last_modified_epoch=last_modified_epoch,
            failed_to_clone=failed_to_clone,
            table_type=target_table_type,
            execution_runtime_ms=execution_runtime_ms,
            labels=self._get_request_labels(node),
        )
        self._query_cache_client.confirm_execution(confirmation_request)
        events.fire_debug_event(
            "Confirmed execution for node {}, request_id {}", node.unique_id, request_id
        )

    def prewarm_connections(self) -> None:
        self._adapter_ext.prewarm_connections()

    def close(self) -> None:
        self._adapter_ext.close()

    def _publish_write_only_execution(
        self,
        bypass_response: CacheBypassedResponse,
        outcome: execution_service_models.ExecutionOutcome,
    ) -> None:
        record = execution_service_models.ExecutionRecord(outcome=outcome)

        original_request = bypass_response.request
        if isinstance(original_request, sql_service_models.SubmitEnrichedSQLRequest):
            if bypass_response.speculative:
                original_request = self._finalize_speculative_request(
                    bypass_response.node, original_request
                )
            record.enriched_sql = execution_service_models.SQLExecution.from_submit_sql_request(
                original_request
            )
            record.enriched_sql.from_speculative_submit = bypass_response.speculative
        else:
            record.values = execution_service_models.ValuesExecution.from_submit_values_request(
                original_request
            )

        try:
            req = execution_service_models.RecordExecutionsRequest(records=[record])
            self._query_cache_client.record_executions(req)
        except Exception as e:
            events.fire_debug_event(
                "Unable to publish write-only execution record for {}: {}",
                original_request.target_table or bypass_response.node.name,
                str(e),
            )

    def _finalize_speculative_request(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        request: sql_service_models.SubmitEnrichedSQLRequest,
    ) -> sql_service_models.SubmitEnrichedSQLRequest:
        """Fill in real dependency timestamps for a request built speculatively.

        A speculative request is built from whatever timestamps the in-flight prefetch
        had produced, leaving the rest unset. Before the outcome is recorded we block on
        the prefetch and refresh the dependency timestamps so the recorded execution
        reflects the same freshness a normal, non-speculative execution would -- including
        any dbt source freshness overrides, which the speculative build path skips and
        which a re-fetch would otherwise miss if the prefetched value has since expired.
        """
        self._await_prefetch_last_modified()
        table_names = [info.name for info in request.tables]
        if not table_names:
            return request
        overrides = (
            self._resolve_dbt_source_freshness_overrides(node)
            if isinstance(node, ModelNode)
            else {}
        )
        epochs = self._adapter_ext.get_last_modified_epoch(table_names, table_overrides=overrides)
        refreshed = {
            info.name: epochs.get(info.name, info.last_modified_epoch) for info in request.tables
        }
        refreshed_tables = [
            shared_models.TableModifiedInfo(name=name, last_modified_epoch=epoch)  # ty: ignore[invalid-argument-type]
            for name, epoch in refreshed.items()
        ]
        return replace(request, tables=refreshed_tables)

    def on_run_result(self, node: ModelOrSnapshotOrSeedNode, result: RunResult) -> None:
        if not (bypass_response := self._cache_bypass_responses.get(node.unique_id)):
            return

        target_table_type, last_modified_epoch = (
            self._get_target_table_type_and_last_modified_epoch(node)
        )
        if last_modified_epoch is None:
            events.fire_debug_event(
                "Skipping write-only confirmation for node {} due to missing last modified epoch",
                node.unique_id,
            )
            return

        outcome = execution_service_models.ExecutionOutcome(
            last_modified_epoch=last_modified_epoch,
            table_type=target_table_type,
            execution_runtime_ms=int(result.execution_time * 1000),
        )

        self._publish_write_only_execution(bypass_response=bypass_response, outcome=outcome)

    def on_state_request_failed(self, node: ModelOrSnapshotOrTestOrSeedNode) -> None:
        """Invalidates cached metadata for a node's target table after an execution whose
        state request failed or was never made.

        Invoked when a node executed normally but its completion will not be confirmed
        back to the query cache. The execution
        rebuilt the target table, so any locally cached metadata for it is stale. Without
        this, downstream nodes in the same invocation would report the table's pre-build
        `last_modified` timestamp to the server and could incorrectly be skipped.

        Args:
            node: The node that was executed.
        """
        if node.unique_id in self._cache_bypass_responses:
            # write-only executions refresh the cache in on_run_result() instead
            return

        try:
            self._adapter_ext.clear_cache([self._node_to_table(node)])
        except Exception as e:
            events.fire_debug_event(
                "Failed to clear cached metadata for node {}: {}", node.unique_id, str(e)
            )

    def _get_target_table_type_and_last_modified_epoch(
        self, node: ModelOrSnapshotOrTestOrSeedNode
    ) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        target_table = self._node_to_table(node)
        self._adapter_ext.clear_cache([target_table])
        last_modified_epoch = self._get_heuristic_last_modified_epoch(target_table)
        target_table_type = self._node_table_type(node)

        return target_table_type, last_modified_epoch

    def _collect_all_prefetch_tables(
        self, selected_ids: t.Set[str]
    ) -> t.Dict[str, ManifestNode | SourceDefinition]:
        """Collect tables from selected model/snapshot nodes and their dependencies for batch prefetching.

        Args:
            selected_ids: The set of unique IDs for models/snapshots selected for this run.
                When non-empty, only tables relevant to these nodes are collected.
                When empty, all model/snapshot tables are collected (full-project run).
        """
        tables: t.Dict[str, ManifestNode | SourceDefinition] = {}
        source_ids: t.Set[str] = set()
        unselected_model_dep_ids: t.Set[str] = set()

        for node in self._manifest.nodes.values():
            if not isinstance(node, (ModelNode, SnapshotNode)):
                continue
            if selected_ids and node.unique_id not in selected_ids:
                continue
            tables[self._node_to_table(node).sql(dialect=self.dialect)] = node
            model_node_ids, source_node_ids = self._resolve_deps(node)
            source_ids.update(source_node_ids)
            if selected_ids:
                unselected_model_dep_ids.update(model_node_ids - selected_ids)

        for source_id in source_ids:
            source = self._manifest.sources.get(source_id)
            if source is not None:
                tables[self._node_to_table(source).sql(dialect=self.dialect)] = source

        for dep_id in unselected_model_dep_ids:
            dep_node = self._manifest.nodes.get(dep_id)
            if dep_node is None:
                continue
            table = (
                self._node_to_deferred_table(dep_node)
                if self._defer_enabled
                else self._node_to_table(dep_node)
            )
            tables[table.sql(dialect=self.dialect)] = dep_node

        return tables

    def _start_prefetch_last_modified(self) -> None:
        """Kick off the async last-modified prefetch if not already started.

        Reads the globally selected resources and collects relevant model/snapshot/source
        FQNs, then triggers an async prefetch. Does not block on the result; use
        `_await_prefetch_last_modified` to wait for it. Idempotent: subsequent calls
        are no-ops.
        """
        with self._prefetch_tables_lock:
            if self._prefetch_started:
                return
            self._prefetch_started = True
            tables = self._collect_all_prefetch_tables(self._selected_resource_ids)
            if not tables:
                self._prefetch_done = True
                return
            events.fire_debug_event(
                "Prefetching last modified timestamps for {} tables",
                len(tables),
            )
            freshness_overrides = {
                fqn: override
                for fqn, node in tables.items()
                if isinstance(node, SourceDefinition)
                for _, override in self._resolve_dbt_source_freshness_overrides(node).items()
            }
            self._prefetch_future = self._adapter_ext.prefetch_last_modified_epochs(
                tables.keys(), table_overrides=freshness_overrides
            )

    def _await_prefetch_last_modified(self) -> None:
        """Ensure the prefetch has started, then block until it completes.

        Idempotent: once the prefetch has completed, subsequent calls are no-ops.
        """
        if self._prefetch_done:
            return
        self._start_prefetch_last_modified()
        with self._prefetch_tables_lock:
            future = self._prefetch_future
        if future is not None:
            future.result()
        self._prefetch_done = True

    def _is_prefetch_ready(self) -> bool:
        """Whether the prefetch has completed, or there is nothing to prefetch.

        Returns False when the prefetch has not been started yet: callers decide whether
        to speculate only after starting it (see ``_start_prefetch_last_modified``), so an
        unstarted prefetch is not "ready".
        """
        with self._prefetch_tables_lock:
            if not self._prefetch_started:
                return False
            future = self._prefetch_future
            return self._prefetch_done or future is None or future.done()

    def _commit_if_open(self) -> None:
        self._adapter.connections.get_thread_connection().transaction_open = True
        self._adapter.commit_if_has_connection()

    def _on_data_test_query(
        self,
        node: ModelOrSnapshotOrTestNode,
        test_sql: str,
        original_op: t.Callable[[], t.Tuple[AdapterResponse, agate.Table]],
    ) -> t.Tuple[AdapterResponse, agate.Table]:
        """Called during the execution of a data test to determine whether to execute the test SQL or return results from the query cache.

        Args:
            node: The test node being executed.
            test_sql: The compiled SQL of the test.
            original_op: The original operation to execute on cache miss.

         Returns:
            A tuple of AdapterResponse and agate.Table.
        """
        query_cache_response = self._submit_sql_request(
            node, sql=test_sql, execution_type=shared_models.ModelExecutionType.DBT_DATA_TEST
        )
        if isinstance(
            query_cache_response, (sql_service_models.ReadyToExecuteResponse, CacheBypassedResponse)
        ):
            start = perf_counter()
            adapter_response, agate_table = original_op()
            elapsed_ms = int((perf_counter() - start) * 1000)
            if agate_table is not None and len(agate_table) == 1:
                results = dict(agate_table[0])
                results = {k.lower(): v for k, v in results.items()}

                if isinstance(query_cache_response, CacheBypassedResponse):
                    self._publish_write_only_execution(
                        bypass_response=query_cache_response,
                        outcome=execution_service_models.ExecutionOutcome(
                            last_modified_epoch=None,
                            table_type=None,
                            execution_results=results,
                            execution_runtime_ms=elapsed_ms,
                        ),
                    )
                else:
                    request_id = query_cache_response.request_id
                    confirmation_request = execution_service_models.ConfirmExecutionRequest(
                        request_id=request_id,
                        last_modified_epoch=None,
                        failed_to_clone=False,
                        table_type=None,
                        execution_results=results,
                        execution_runtime_ms=elapsed_ms,
                        labels=self._get_request_labels(node),
                    )
                    self._query_cache_client.confirm_execution(confirmation_request)
                    events.fire_debug_event(
                        "Confirmed execution for test {}, request_id {}", node.unique_id, request_id
                    )
            return adapter_response, agate_table
        if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
            events.fire_debug_event("Received skip execution response for node {}", node.name)
            self._record_cache_hit(query_cache_response)
            agate_table = agate.Table.from_object(  # ty: ignore[unresolved-attribute]
                [query_cache_response.execution_results],
                column_types={
                    "failures": agate_helper.Integer(),
                    "should_error": agate.Boolean(),
                    "should_warn": agate.Boolean(),
                },
            )
            adapter_response = AdapterResponse(_message=NO_OP_STATUS)
            return adapter_response, agate_table
        events.fire_warn_event_with_cache_bypass(
            "Unexpected dbt State response type for test '{}': {}",
            node.unique_id,
            type(query_cache_response).__name__,
        )
        return original_op()

    def _process_query_cache_response(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        query_cache_response: t.Union[
            sql_service_models.ReadyToExecuteResponse,
            sql_service_models.SkipExecutionResponse,
            clone_service_models.ReadyToCloneResponse,
            CacheBypassedResponse,
            None,
        ],
    ) -> t.Union[RunResult, NoRunResult, None]:
        if query_cache_response is None:
            return None

        if isinstance(query_cache_response, CacheBypassedResponse):
            # these get picked up in RunCache.on_run_result() when the execution completes
            self._cache_bypass_responses[node.unique_id] = query_cache_response
            return None

        explained_decision = query_cache_response.explained_decision
        explain_message = ExplainMessageEntry(
            execution_decision_id=query_cache_response.execution_decision_id or "",
            decision=explained_decision.decision,
            decision_description=explained_decision.decision_description,
        )
        if explain_message.decision_description:
            events.fire_debug_event(
                "Explained state decision for node '{}': {}",
                node.name,
                explain_message.decision_description,
            )
        is_stale = explained_decision.is_stale
        clone_run_status, clone_message = self._clone_status_and_message(is_stale)
        if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
            events.fire_debug_event("Received skip execution response for node {}", node.name)
            self._record_cache_hit(query_cache_response)
            should_run_hooks = self._run_cache_config.resolve_run_hooks_on_no_op(node.config)
        elif isinstance(query_cache_response, clone_service_models.ReadyToCloneResponse):
            events.fire_debug_event(
                "Received ready to clone response for node {}, request_id: {}",
                node.name,
                query_cache_response.request_id,
            )
            should_run_hooks = True
        else:
            events.fire_debug_event(
                "Received execute response for node {}, request_id: {}",
                node.name,
                query_cache_response.request_id,
            )
            return NoRunResult(query_cache_response.request_id, failed_to_clone=False)

        # Note: pre-hooks run before the try block. On clone failure, dbt's fallback
        # materialization will re-run them. This is acceptable since clone failures are exceptional.
        context = None
        if should_run_hooks:
            context = generate_runtime_model_context(node, self._config, self._manifest)
            context_config = context["config"]
            hook_ctx = self._adapter.pre_model_hook(context_config)
            self._run_hooks(getattr(node.config, "pre_hook", []), context)

        try:
            if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
                if node.unique_id in self._dev_cloned_nodes:
                    return RunResult.from_node(
                        node,
                        clone_run_status,
                        clone_message,
                    )
                # SkipExecutionResponse is only produced for models/snapshots/tests,
                # not seeds — narrow the type for resolve_freshness_tolerance.
                reused_status, reused_message = self._no_op_status_and_message(
                    is_stale,
                    t.cast("t.Union[ModelConfig, SnapshotConfig, TestConfig]", node.config),
                )
                return RunResult.from_node(
                    node,
                    reused_status,
                    reused_message,
                )
            if query_cache_response.clone_required_last_modified_epoch is not None:
                current_last_modified_epoch = self._get_last_modified_epoch(
                    exp.to_table(query_cache_response.clone_source, dialect=self.dialect)
                )
                if current_last_modified_epoch is None or (
                    current_last_modified_epoch
                    > query_cache_response.clone_required_last_modified_epoch
                ):
                    events.fire_debug_event(
                        "Unable to clone node '{}' due to table's latest state not matching what is expected. "
                        "Expected last modified epoch: {}, actual last modified epoch: {}.",
                        node.name,
                        query_cache_response.clone_required_last_modified_epoch,
                        current_last_modified_epoch,
                    )
                    should_run_hooks = False
                    return NoRunResult(query_cache_response.request_id, failed_to_clone=True)
            with events.downgrade_adapter_error_events():
                if self._adapter_ext.IMPLEMENTS_CUSTOM_CLONE:
                    self._adapter_ext.clone(
                        query_cache_response.clone_sqls,
                        query_cache_response.clone_source,
                        query_cache_response.clone_target,
                    )
                else:
                    for sql in query_cache_response.clone_sqls:
                        self._adapter.execute(sql)
            self._commit_if_open()
            # when we clone a table, we put it in the relation cache so that the remainder of the
            # invocation knows it exists without hitting the db
            self._adapter_ext.cache_node_relation(node)
            self.confirm_execution(node, query_cache_response.request_id)
            self._record_cache_hit(query_cache_response)
            return RunResult.from_node(
                node,
                clone_run_status,
                clone_message,
            )
        except Exception as e:
            self._adapter_ext.rollback()
            should_run_hooks = False
            if isinstance(query_cache_response, clone_service_models.ReadyToCloneResponse):
                events.fire_warn_event(
                    "Clone failed for node '{}', falling back to full execution: {}",
                    node.name,
                    str(e),
                )
                return NoRunResult(query_cache_response.request_id, failed_to_clone=True)
            raise
        finally:
            if should_run_hooks:
                self._run_hooks(getattr(node.config, "post_hook", []), context)
                self._commit_if_open()
                self._adapter.post_model_hook(context_config, hook_ctx)

    def _run_hooks(self, hooks: t.List[t.Any], context: t.Dict[str, t.Any]) -> None:
        for hook in hooks:
            rendered_sql = get_rendered(hook.sql, context)
            if rendered_sql.strip():
                self._adapter.execute(rendered_sql, auto_begin=hook.transaction)

    def _try_clone(self, node: ModelOrSnapshotNode) -> bool:
        if self._dev_cloner is None or self.is_write_only:
            return False
        clone_response = self._submit_clone_request(node)
        if clone_response is None:
            return False

        if isinstance(clone_response, clone_service_models.UnableToCloneResponse):
            clone_rejection_reason = clone_response.explained_decision.clone_rejection_reason
            events.fire_debug_event(
                f"Unable to clone {clone_response.clone_source}: {clone_rejection_reason}"
            )
            return False

        self._dev_cloner.clone(
            self._adapter,
            node,
            clone_response.clone_sqls,
            clone_response.clone_source,
            clone_response.clone_target,
        )
        self._commit_if_open()
        if isinstance(clone_response, clone_service_models.ReadyToCloneResponse):
            self.confirm_execution(node, clone_response.request_id)
            self._decision_logger.log_dev_clone(
                node.name, clone_response.clone_source, clone_response.clone_target
            )
        return True

    def _submit_sql_speculative(
        self,
        node: ModelOrSnapshotOrTestNode,
        request: sql_service_models.SubmitEnrichedSQLRequest,
        request_id: str,
    ) -> t.Union[
        sql_service_models.SkipExecutionResponse,
        clone_service_models.ReadyToCloneResponse,
        sql_service_models.ReadyToExecuteUntrackedResponse,
        None,
    ]:
        """Issue a speculative submit and map the verdict onto an actionable response.

        Returns Skip/Clone responses to act on immediately, the ReadyToExecuteUntrackedResponse
        itself for an untracked-execute verdict (the caller must await the prefetch and rebuild
        the request with real timestamps before recording it), or None to signal that the caller
        must block on the prefetch and resubmit non-speculatively (undecided verdict, or any
        speculative error/timeout).
        """
        try:
            response = self._query_cache_client.submit_sql_speculative(request, request_id)
        except Exception as e:
            events.fire_debug_event("Speculative submit failed for node {}: {}", node.name, str(e))
            return None

        events.fire_debug_event(
            "Speculative submit for node {} returned {}", node.name, type(response).__name__
        )
        if isinstance(
            response,
            (sql_service_models.SkipExecutionResponse, clone_service_models.ReadyToCloneResponse),
        ):
            if response.execution_decision_id:
                self._decision_logger.log_execution_decision_id(
                    node_name=node.name, execution_decision_id=response.execution_decision_id
                )
            return response
        if isinstance(response, sql_service_models.ReadyToExecuteUntrackedResponse):
            return response
        # Undecided, or any unexpected response type: block on the prefetch and resubmit.
        return None

    def _submit_sql_request(
        self,
        node: ModelOrSnapshotOrTestNode,
        sql: t.Optional[str] = None,
        execution_type: t.Optional[shared_models.ModelExecutionType] = None,
        microbatch_window: t.Optional[t.Tuple[datetime, datetime]] = None,
    ) -> t.Union[
        sql_service_models.ReadyToExecuteResponse,
        sql_service_models.SkipExecutionResponse,
        clone_service_models.ReadyToCloneResponse,
        CacheBypassedResponse,
        None,
    ]:
        request_id = uuid.uuid4().hex
        request_start_time = perf_counter()
        try:
            self._start_prefetch_last_modified()

            # Resolve inputs and run the (prefetch-independent) view traversal up front. The
            # traversal blocks on view-definition fetches while the async last-modified prefetch
            # runs concurrently, so deferring the speculative decision until afterwards lets us
            # take the accurate non-speculative path for free whenever the prefetch completed
            # during the traversal window.
            resolved_sql = sql or node.compiled_code or ""
            if not resolved_sql:
                raise RuntimeError(f"Model node '{node.unique_id}' must be compiled")
            resolved_execution_type = execution_type or shared_models.ModelExecutionType(
                self._node_execution_type(node)
            )
            traversal_result: t.Optional[ViewTraversalResult] = None
            view_traversal_duration_ms: t.Optional[int] = None
            if resolved_execution_type != shared_models.ModelExecutionType.VIEW:
                view_traversal_start = perf_counter()
                traversal_result = self._adapter_ext.traverse_view_definitions(resolved_sql)
                view_traversal_duration_ms = int((perf_counter() - view_traversal_start) * 1000)

            use_speculative = not self.is_write_only and not self._is_prefetch_ready()
            if not use_speculative:
                self._await_prefetch_last_modified()

            request, last_modified_duration_ms = self._build_submit_enriched_sql_request(
                node,
                resolved_sql,
                resolved_execution_type,
                traversal_result=traversal_result,
                microbatch_window=microbatch_window,
                speculative=use_speculative,
            )
            request_end_time = perf_counter()
            duration = request_end_time - request_start_time

            self._emit_enriched_sql_prepared_telemetry(
                request_id,
                duration,
                target_table_fqn=node.relation_name,
                labels=self._get_request_labels(node),
                num_dependencies=len(request.tables) - 1,  # exclude the target table in count
                num_view_dependencies=len(request.query_dependencies),
                view_traversal_duration_ms=view_traversal_duration_ms,
                last_modified_duration_ms=last_modified_duration_ms,
            )

            if self.is_write_only:
                # todo: does a cache bypass still need to submit telemetry?
                # technically the "enriched" SQL was still prepared, we just didnt use it to ask for a cache decision
                return CacheBypassedResponse(request, node)

            if use_speculative:
                events.fire_debug_event(
                    "Prefetch still in flight for node {}; submitting speculatively", node.name
                )
                speculative_result = self._submit_sql_speculative(node, request, request_id)
                if isinstance(
                    speculative_result,
                    (
                        sql_service_models.SkipExecutionResponse,
                        clone_service_models.ReadyToCloneResponse,
                    ),
                ):
                    return speculative_result
                if isinstance(
                    speculative_result, sql_service_models.ReadyToExecuteUntrackedResponse
                ):
                    # Execute the node now; its outcome is recorded after the fact with real
                    # timestamps (finalized against the completed prefetch) via RecordExecutions.
                    return CacheBypassedResponse(request, node, speculative=True)
                # Undecided verdict or a speculative error: block on the prefetch and resubmit
                # a non-speculative request built with real timestamps. Reuse the traversal
                # already computed above rather than walking the view graph again.
                self._await_prefetch_last_modified()
                request, _ = self._build_submit_enriched_sql_request(
                    node,
                    resolved_sql,
                    resolved_execution_type,
                    traversal_result=traversal_result,
                    microbatch_window=microbatch_window,
                    speculative=False,
                )

            response = self._query_cache_client.submit_sql(request, request_id)
            if response.execution_decision_id:
                self._decision_logger.log_execution_decision_id(
                    node_name=node.name, execution_decision_id=response.execution_decision_id
                )

            return response

        except Exception as e:
            request_end_time = perf_counter()
            self._log_submit_sql_error(e, node)
            duration = request_end_time - request_start_time
            self._emit_enriched_sql_prepared_telemetry(
                request_id,
                duration=duration,
                target_table_fqn=node.relation_name,
                labels=self._get_request_labels(node),
                num_dependencies=None,
                num_view_dependencies=None,
                error_type=type(e).__name__,
            )
            if isinstance(e, grpc.RpcError):
                raise

        return None

    def _submit_values_request(
        self,
        node: SeedNode,
    ) -> t.Union[
        sql_service_models.ReadyToExecuteResponse,
        sql_service_models.SkipExecutionResponse,
        clone_service_models.ReadyToCloneResponse,
        CacheBypassedResponse,
        None,
    ]:
        request_id = uuid.uuid4().hex
        try:
            request = self._build_submit_values_request(node)

            if self.is_write_only:
                return CacheBypassedResponse(request, node)

            response = self._query_cache_client.submit_values(request, request_id)
            if response.execution_decision_id:
                self._decision_logger.log_execution_decision_id(
                    node_name=node.name, execution_decision_id=response.execution_decision_id
                )
            return response
        except Exception as e:
            events.fire_warn_event_with_cache_bypass(
                "Error preparing values request for seed '{}': {}",
                node.name,
                str(e),
            )
            if isinstance(e, grpc.RpcError):
                raise
        return None

    @staticmethod
    def _validate_positive_int(value: t.Any, field_name: str) -> t.Optional[int]:
        if value is None:
            return None
        value = int(value)
        if value <= 0:
            events.fire_warn_event("Invalid {}={} (must be > 0), ignoring", field_name, value)
            return None
        return value

    def _get_table_properties(
        self, node: ModelOrSnapshotOrTestOrSeedNode
    ) -> t.Optional[TableProperties]:
        hours = self._validate_positive_int(
            node.config.extra.get("hours_to_expiration"), "hours_to_expiration"
        )
        partition_days = self._validate_positive_int(
            node.config.extra.get("partition_expiration_days"),
            "partition_expiration_days",
        )
        if hours is None and partition_days is None:
            return None
        return TableProperties(
            hours_to_expiration=hours,
            partition_expiration_days=partition_days,
        )

    def _build_submit_values_request(
        self,
        node: SeedNode,
    ) -> sql_service_models.SubmitValuesRequest:
        node_config = node.config
        semantic_extras = {
            key: _serialize_semantic_extra(key, node_config.get(key))
            for key in SEED_SEMANTIC_EXTRAS_CONFIG_KEYS
            if key in node_config
        }
        semantic_extras.update(self._persisted_docs_semantic_extras(node))
        last_modified_epoch = self._get_last_modified_epoch(self._node_to_table(node))

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
            dialect=self._adapter.type(),
            default_catalog=self._adapter_ext.default_catalog,
            values_hash=calculator.calculate_node_hash(),
            semantic_extras=semantic_extras,
            last_modified_epoch=last_modified_epoch,
            labels=self._get_request_labels(node),
            clone_time_travel_limit=self._clone_time_travel_limit,
            clone_table_properties=self._get_table_properties(node),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
            dbt_node_state=dbt_node_state,
        )

    def _emit_enriched_sql_prepared_telemetry(
        self,
        request_id: str,
        duration: float,
        target_table_fqn: t.Optional[str],
        labels: t.Dict[str, str],
        num_dependencies: t.Optional[int] = None,
        num_view_dependencies: t.Optional[int] = None,
        error_type: t.Optional[str] = None,
        view_traversal_duration_ms: t.Optional[int] = None,
        last_modified_duration_ms: t.Optional[int] = None,
    ) -> None:
        try:
            enriched_sql_request = client_telemetry_service_models.ClientPrepareEnrichedSQLRequest(
                request_id=request_id,
                duration=duration,
                target_table_fqn=target_table_fqn,
                num_dependencies=num_dependencies,
                num_view_dependencies=num_view_dependencies,
                error_type=error_type,
                view_traversal_duration_ms=view_traversal_duration_ms,
                last_modified_duration_ms=last_modified_duration_ms,
                labels=labels,
            )
            self._telemetry_dispatcher.add_event(enriched_sql_request)
        except Exception as e:
            events.fire_debug_event(
                "Failed to emit enriched SQL telemetry: {} ({})", type(e).__name__, str(e)
            )

    def _log_submit_sql_error(self, e: Exception, node: ModelOrSnapshotOrTestNode) -> None:
        node_type = (
            "test"
            if isinstance(node, (GenericTestNode, SingularTestNode))
            else "snapshot"
            if isinstance(node, SnapshotNode)
            else "model"
        )
        if isinstance(e, SqlglotError):
            events.fire_warn_event_with_cache_bypass(
                "Failed to parse compiled SQL for {} '{}': {}",
                node_type,
                node.name,
                str(e),
            )
        elif isinstance(e, (ValueError, TypeError, AttributeError, KeyError)):
            events.fire_warn_event_with_cache_bypass(
                "Data validation error preparing enriched SQL for {} '{}': {}",
                node_type,
                node.name,
                str(e),
            )
        elif isinstance(e, RuntimeError):
            events.fire_warn_event_with_cache_bypass(
                "Runtime error preparing enriched SQL for {} '{}': {}",
                node_type,
                node.name,
                str(e),
            )
        else:
            events.fire_warn_event_with_cache_bypass(
                "Error preparing enriched SQL for {} '{}': {}",
                node_type,
                node.name,
                str(e),
            )

    def _submit_clone_request(
        self, node: ModelOrSnapshotNode
    ) -> t.Optional[
        t.Union[
            clone_service_models.ReadyToCloneResponse, clone_service_models.UnableToCloneResponse
        ]
    ]:
        assert self._dev_cloner is not None
        result = self._dev_cloner.get_clone_source(node)
        if not result:
            return None
        clone_source, clone_source_table_type = result
        clone_request = self._build_clone_request(node, clone_source, clone_source_table_type)
        return self._query_cache_client.register_clone(clone_request)

    def _build_submit_enriched_sql_request(
        self,
        node: ModelOrSnapshotOrTestNode,
        sql: str,
        execution_type: shared_models.ModelExecutionType,
        traversal_result: t.Optional[ViewTraversalResult],
        microbatch_window: t.Optional[t.Tuple[datetime, datetime]] = None,
        speculative: bool = False,
    ) -> t.Tuple[sql_service_models.SubmitEnrichedSQLRequest, int]:
        target_table = (
            self._node_to_table(node).sql(dialect=self.dialect)
            if execution_type != shared_models.ModelExecutionType.DBT_DATA_TEST
            else None
        )
        dialect = self._adapter.type()
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
            return sql_service_models.SubmitEnrichedSQLRequest(
                tables=table_infos,
                query_dependencies=[],
                target_table=target_table,
                dialect=dialect,
                default_catalog=default_catalog,
                default_schema=self._adapter_ext.DEFAULT_SCHEMA_NAME,
                execution_type=execution_type,
                sql=sql,
                semantic_extras=self._persisted_docs_semantic_extras(node),
                freshness_tolerance_seconds=0,
                lenient_dependencies=set(),
                tolerate_nondeterminism=True,
                labels=self._get_request_labels(node),
                clone_time_travel_limit=self._clone_time_travel_limit,
                clone_table_properties=self._get_table_properties(node),
                stale_upstream_policy=self._run_cache_config.resolve_stale_upstream_policy(
                    node_config
                ),
                clone_chain_depth_limit=self.clone_chain_depth_limit,
                dbt_node_state=self._build_dbt_node_state(node),
                compare_unrendered_code=self._run_cache_config.resolve_compare_unrendered_code(
                    node_config
                ),
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
                self._resolve_dbt_source_freshness_overrides(node)
                if isinstance(node, ModelNode)
                else {}
            )
            overrides.update(source_freshness_overrides)

            unresolvable = traversal_result.unresolvable_tables
            if unresolvable:
                self._adapter_ext.clear_last_modified_cache(unresolvable)
                now_ms = self._get_heuristic_now_epoch()
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

        table_infos = [
            shared_models.TableModifiedInfo(name=name, last_modified_epoch=epoch)  # ty: ignore[invalid-argument-type]
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

        if self._run_cache_config.enable_lenient_dependencies:
            all_seen_fqns = traversal_result.seen_tables | set(traversal_result.view_definitions)
            lenient_dependencies: t.Set[str] = self._deferred_fqns & all_seen_fqns
        else:
            lenient_dependencies = set()

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
        semantic_extras.update(self._persisted_docs_semantic_extras(node))
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
            lenient_dependencies=lenient_dependencies,
            tolerate_nondeterminism=self._run_cache_config.resolve_tolerate_nondeterminism(
                node_config
            ),
            labels=self._get_request_labels(node),
            clone_time_travel_limit=self._clone_time_travel_limit,
            clone_table_properties=self._get_table_properties(node),
            stale_upstream_policy=self._run_cache_config.resolve_stale_upstream_policy(node_config),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
            dbt_node_state=self._build_dbt_node_state(node),
            compare_unrendered_code=self._run_cache_config.resolve_compare_unrendered_code(
                node_config
            ),
        ), last_modified_duration_ms

    def _build_clone_request(
        self,
        node: ModelOrSnapshotOrTestNode,
        clone_source: str,
        clone_source_table_type: t.Optional[str],
    ) -> clone_service_models.CloneRequest:
        clone_source_last_modified_epoch = self._get_last_modified_epoch(
            exp.to_table(clone_source, dialect=self.dialect)
        )
        return clone_service_models.CloneRequest(
            target_table=node.relation_name or "",
            clone_source_table=clone_source,
            dialect=self.dialect,
            default_catalog=self._adapter_ext.default_catalog,
            execution_type=shared_models.ModelExecutionType(self._node_execution_type(node)),
            clone_source_last_modified_epoch=clone_source_last_modified_epoch,
            labels=self._get_request_labels(node),
            clone_source_table_type=clone_source_table_type,
            table_properties=self._get_table_properties(node),
            clone_chain_depth_limit=self.clone_chain_depth_limit,
        )

    @staticmethod
    def _get_request_labels(node: ModelOrSnapshotOrTestOrSeedNode) -> t.Dict[str, str]:
        unique_id = node.unique_id

        return {
            "dbt_node_name": node.name,
            "dbt_node_fqn": ".".join(node.fqn),
            "dbt_node_unique_id": unique_id,
        }

    def _persisted_docs_semantic_extras(
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

    def _build_dbt_node_state(self, node: ModelOrSnapshotOrTestNode) -> shared_models.DbtNodeState:
        calculator = create_node_hash_calculator(node, self._manifest, self._config)

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
        )

    def _node_execution_type(self, node: ModelOrSnapshotOrTestNode) -> str:
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

    def _node_table_type(self, node: ModelOrSnapshotOrTestOrSeedNode) -> t.Optional[str]:
        # note: get_relation() only returns a relation for relations that exist
        # it's intended that the table type is determined *after* dbt has created the tables, not before
        if (
            relation := self._adapter.get_relation(
                database=node.database, schema=node.schema, identifier=node.identifier
            )
        ) and isinstance(relation, BaseRelation):
            return self._adapter_ext.get_relation_table_type(node=node, relation=relation)

        return None

    def _get_heuristic_now_epoch(self) -> t.Optional[int]:
        if self._engine_heuristics_clock_disabled:
            return None

        try:
            return self._engine_heuristics_clock.now_utc_epoch()
        except Exception as e:
            events.fire_debug_event(
                "Failed to get heuristic epoch: {}; disabling heuristic clock",
                str(e),
            )
            self._engine_heuristics_clock_disabled = True

    def _get_heuristic_last_modified_epoch(self, table: exp.Table) -> t.Optional[int]:
        if not self._use_heuristic_clock_for_last_modified:
            return self._get_last_modified_epoch(table)

        if heuristic_now_millis := self._get_heuristic_now_epoch():
            self._adapter_ext.cache_last_modified_epoch(table, heuristic_now_millis)
            return heuristic_now_millis
        events.fire_debug_event(
            "Failed to get heuristic last modified for table '{}', falling back to warehouse query",
            table.sql(dialect=self.dialect),
        )
        self._use_heuristic_clock_for_last_modified = False
        return self._get_last_modified_epoch(table)

    def _get_last_modified_epoch(self, table: exp.Table) -> t.Optional[int]:
        last_modified_epochs = self._adapter_ext.get_last_modified_epoch([table])
        if len(last_modified_epochs) != 1:
            raise RuntimeError("Expected exactly one table info")
        last_modified_epoch = next(iter(last_modified_epochs.values()))
        if last_modified_epoch is None:
            events.fire_debug_event(
                "Failed to get last modified for table: '{}'", table.sql(dialect=self.dialect)
            )
        return last_modified_epoch

    def _node_to_table(self, node: ManifestNode | SourceDefinition) -> exp.Table:
        return self._adapter_ext._node_to_table(node)

    def _sql(self, expr: exp.Expr, copy: bool = False) -> str:
        return self._adapter_ext._sql(expr, copy=copy)

    def _node_to_deferred_table(self, node: ManifestNode) -> exp.Table:
        assert self._deferred_relation_resolver is not None
        database = self._deferred_relation_resolver.get_deferred_database(node) or node.database
        schema = self._deferred_relation_resolver.get_deferred_schema(node) or node.schema
        identifier = self._deferred_relation_resolver.get_deferred_identifier(node) or node.alias

        return self._adapter_ext._node_to_table(
            node, override_database=database, override_schema=schema, override_identifier=identifier
        )

    def _record_cache_hit(
        self,
        response: t.Union[
            sql_service_models.SkipExecutionResponse, clone_service_models.ReadyToCloneResponse
        ],
    ) -> None:
        self._total_cache_hits += 1
        self._total_time_saved_ms += response.execution_runtime_ms or 0

    def _resolve_deps(self, node: ManifestSQLNode) -> t.Tuple[t.Set[str], t.Set[str]]:
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

    def _defer_relation(self, relation: BaseRelation, target_node: ManifestNode) -> BaseRelation:
        assert self._deferred_relation_resolver is not None
        deferred_relation = replace(relation, path=replace(relation.path))
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

    def _resolve_dbt_source_freshness_overrides(
        self, node: ModelNode | SourceDefinition
    ) -> t.Dict[str, t.Callable[[], int]]:
        """Users can configure source freshness in their project by adding a `freshness:` block to the source
        definitions. They can either specify a timestamp column to use or a custom query to run.

        In normal dbt, these only get invoked if the user runs `dbt source freshness`.
        However in run-cache we want to treat this logic as an override to our default method of determining source freshness.

        So, given a model node, this function packages up any freshness overrides on its sources into functions that,
        when executed, return a run-cache compatible last_modified_epoch.

        Docs: https://docs.getdbt.com/reference/resource-properties/freshness?version=1.12

        params:
            node: a ModelNode that may or may not have {{ source() }} blocks in it

        returns:
            A dict of source fqn -> function to call that will run dbt freshness and return a run-cache compatible last_modified_epoch.
            Only sources with freshness overrides specified in user config are returned.
        """

        if isinstance(node, ModelNode):
            _, source_ids = self._resolve_deps(node)
            source_definitions = list(
                filter(None, [self._manifest.sources.get(source_id) for source_id in source_ids])
            )
        else:
            source_definitions = [node]

        overrides = {}
        for defn in source_definitions:
            if hasattr(defn, "loaded_at_query"):
                # loaded_at_query doesnt exist until dbt 1.10 and takes precedence over loaded_at_field
                if defn.loaded_at_query is None and defn.loaded_at_field is None:
                    continue
            elif defn.loaded_at_field is None:
                continue

            relation = self._adapter_ext._node_to_relation(defn)

            # note: these are deliberately bound as defaults so that the correct value is captured in each _run_freshness() function
            def _run_freshness(
                defn: SourceDefinition = defn, relation: BaseRelation = relation
            ) -> int:
                # logic adapted from: https://github.com/dbt-labs/dbt-core/blob/c02340d4c14df1459c00cf91b9ab738e1c4c9507/core/dbt/task/freshness.py#L120
                if hasattr(defn, "loaded_at_query") and defn.loaded_at_query:
                    # only present if loaded_at_query is present, dbt >= 1.10
                    from dbt.context.providers import SourceContext

                    compiled_code = get_rendered(
                        defn.loaded_at_query,
                        SourceContext(
                            defn, self._config, self._manifest, RuntimeProvider(), None
                        ).to_dict(),
                        defn,
                    )
                    _, freshness = self._adapter_ext.adapter.calculate_freshness_from_custom_sql(
                        relation,
                        compiled_code,
                        macro_resolver=self._manifest,
                    )
                elif defn.loaded_at_field:
                    _, freshness = self._adapter_ext.adapter.calculate_freshness(
                        relation,
                        defn.loaded_at_field,
                        defn.freshness.filter if defn.freshness else None,
                        self._manifest,
                    )
                else:
                    raise ValueError(
                        f"No custom freshness metadata defined for {relation.render()}; execution should not have reached here"
                    )

                # the returned datetimes are not naive so this works
                user_last_modified_epoch = int(freshness["max_loaded_at"].timestamp() * 1000)

                # note: we use the heuristic clock instead of adapter_ext.current_timestamp_utc() to avoid the overhead of another db query
                if now_epoch := self._get_heuristic_now_epoch():
                    # verify the value isnt far in the future. if a far future value gets cached,
                    # and then the user fixes their freshness query to return a reasonable value,
                    # run-cache will keep returning Skip responses because the new value will always
                    # be older than the original value
                    if user_last_modified_epoch > now_epoch:
                        events.fire_warn_event(
                            "Custom last_modified query for {} returned a timestamp in the future: {}. "
                            "This indicates a bug in the query. Trimming it to the current timestamp: {}.",
                            relation.render(),
                            user_last_modified_epoch,
                            now_epoch,
                        )
                        user_last_modified_epoch = now_epoch

                return user_last_modified_epoch

            source_fqn = self._sql(self._node_to_table(defn))
            overrides[source_fqn] = _run_freshness

        return overrides

    def _cache_hit_run_status(self) -> RunStatus:
        """Return the ``RunStatus`` to use for cache-hit results (no-op or clone).

        ``RunStatus.Reused`` when ``emit_reused_status`` is enabled and the running
        dbt-core supports it; otherwise ``RunStatus.Success``. Emits a single warn
        event if the flag is on but the installed dbt build pre-dates the enum.
        """
        if not self._run_cache_config.emit_reused_status:
            return RunStatus.Success
        if _RUN_STATUS_REUSED is None:
            if not self._reused_status_warning_emitted:
                events.fire_warn_event(
                    "emit_reused_status is enabled but the installed dbt version "
                    "does not support RunStatus.Reused; falling back to Success."
                )
                self._reused_status_warning_emitted = True
            return RunStatus.Success
        return _RUN_STATUS_REUSED

    def _clone_status_and_message(self, is_stale: bool) -> t.Tuple[RunStatus, str]:
        """Return (status, message) for cache-hit clone results.

        When ``emit_reused_status`` is enabled and the running dbt-core supports
        ``RunStatus.Reused``, emit the new status with a Fusion-style message
        describing the clone. Otherwise fall back to the legacy ``Success`` +
        "CLONE" representation so older dbt clients keep working.
        """
        status = self._cache_hit_run_status()
        if status is _RUN_STATUS_REUSED and _RUN_STATUS_REUSED is not None:
            suffix = " within tolerance" if is_stale else ""
            return status, "Cloned from other environment" + suffix
        legacy_suffix = " (within tolerance)" if is_stale else ""
        return status, "CLONE" + legacy_suffix

    def _no_op_status_and_message(
        self,
        is_stale: bool,
        node_config: t.Union["ModelConfig", "SnapshotConfig", "TestConfig"],
    ) -> t.Tuple[RunStatus, str]:
        """Return (status, message) for cache-hit no-op results.

        When ``emit_reused_status`` is enabled and the running dbt-core supports
        ``RunStatus.Reused``, emit the new status with a Fusion-style message
        describing why the node was reused. Otherwise fall back to the legacy
        ``Success`` + "NO-OP" representation so older dbt clients keep working.
        """
        status = self._cache_hit_run_status()
        if status is not _RUN_STATUS_REUSED:
            freshness_suffix = " (within tolerance)" if is_stale else ""
            return status, NO_OP_STATUS + freshness_suffix
        if is_stale:
            tolerance_seconds = self._run_cache_config.resolve_freshness_tolerance(node_config)
            message = (
                f"New changes detected within freshness tolerance of "
                f"{humanize.naturaldelta(tolerance_seconds)}"
            )
        else:
            message = "No new changes"
        return status, message

    @cached_property
    def _selected_resource_ids(self) -> t.Set[str]:
        from dbt.selected_resources import SELECTED_RESOURCES

        return set(SELECTED_RESOURCES)

    @property
    def _adapter(self) -> SQLAdapter:
        return self._adapter_ext.adapter

    @property
    def _defer_enabled(self) -> bool:
        if self._deferred_relation_resolver is None:
            return False
        # defer should always be considered enabled (for RunCache plugin purposes) unless --no-defer was explicitly provided by the user
        # note that we have to check sys.argv because:
        # - the original cli args are not available on RuntimeConfig
        # - RuntimeConfig.args.defer defaults to False which means we cannot tell the difference between the default and a explicitly supplied --no-defer argument
        return "--no-defer" not in sys.argv

    @property
    def dialect(self) -> str:
        return self._adapter.type()

    @property
    def run_cache_config(self) -> RunCacheConfig:
        return self._run_cache_config

    @property
    def total_cache_hits(self) -> int:
        return self._total_cache_hits

    @property
    def total_time_saved_ms(self) -> int:
        return self._total_time_saved_ms

    @property
    def clone_chain_depth_limit(self) -> t.Optional[int]:
        default_limit = self._adapter_ext.CLONE_CHAIN_DEPTH_LIMIT

        # in prod, we set 1 less than the actual limit (which may force an execute instead of a clone)
        # this ensures that there is always at least 1 more clone left for a dev clone
        if self._defer_enabled and self._profiles.is_defer_to_profile and default_limit is not None:
            return max(default_limit - 1, 0)

        return default_limit

    @property
    def is_write_only(self) -> bool:
        """Whether or not we are in "write only" mode, which records execution outcomes but does not
        ask the cache to make decisions"""
        return self._run_cache_config.cache_mode.is_write_only


class _DataTestAdapterProxy:
    def __init__(
        self, node: t.Union[GenericTestNode, SingularTestNode], run_cache: RunCache
    ) -> None:
        self._node = node
        self._run_cache = run_cache
        self._adapter = run_cache._adapter
        self._adapter_ext = self._run_cache._adapter_ext
        self._relation_to_drop: t.Optional[BaseRelation] = None

    def __getattr__(self, name: str) -> t.Any:
        return getattr(self._adapter, name)

    def execute(
        self,
        sql: str,
        *args: t.Any,
        **kwargs: t.Any,
    ) -> t.Tuple[AdapterResponse, agate.Table]:
        try:
            parsed_test_sql = parse_one(sql, dialect=self._adapter_ext.dialect)
            named_selects = (
                parsed_test_sql.named_selects if isinstance(parsed_test_sql, exp.Select) else []
            )
            if sorted(named_selects) == ["failures", "should_error", "should_warn"]:
                return self._run_cache._on_data_test_query(
                    self._node,
                    sql,
                    lambda: self._adapter.execute(sql, *args, **kwargs),
                )
            if isinstance(parsed_test_sql, exp.Create) and parsed_test_sql.kind == "TABLE":
                # Handle the CTAS statement which creates a table with data test failures
                cached_run_result = None
                query_cache_response = None
                try:
                    query_cache_response = self._run_cache._submit_sql_request(
                        self._node, sql=sql, execution_type=shared_models.ModelExecutionType.FULL
                    )
                    cached_run_result = self._run_cache._process_query_cache_response(
                        self._node, query_cache_response
                    )
                    if isinstance(cached_run_result, RunResult):
                        # We got a cache hit for the CTAS statement
                        self._adapter.commit_if_has_connection()
                        return AdapterResponse(_message=NO_OP_STATUS), agate.Table.from_object([])  # ty: ignore[unresolved-attribute]
                except Exception as e:
                    events.fire_warn_event_with_cache_bypass(
                        "Error processing dbt State response for test '{}': {}",
                        self._node.unique_id,
                        str(e),
                    )

                execution_start_ts = perf_counter()
                if self._relation_to_drop:
                    # Execute the postponed drop
                    self._adapter.drop_relation(self._relation_to_drop)
                result = self._adapter.execute(sql, *args, **kwargs)
                elapsed_ms = int((perf_counter() - execution_start_ts) * 1000)
                self._adapter_ext.cache_node_relation(self._node)

                try:
                    self._adapter.commit_if_has_connection()
                    self._adapter.connections.begin()
                except Exception as e:
                    events.fire_debug_event(
                        "Error starting a new transaction for test '{}': {}",
                        self._node.unique_id,
                        str(e),
                    )

                if isinstance(query_cache_response, CacheBypassedResponse):
                    table_type, last_modified_epoch = (
                        self._run_cache._get_target_table_type_and_last_modified_epoch(self._node)
                    )
                    self._run_cache._publish_write_only_execution(
                        bypass_response=query_cache_response,
                        outcome=execution_service_models.ExecutionOutcome(
                            last_modified_epoch=last_modified_epoch,
                            table_type=table_type,
                            execution_runtime_ms=elapsed_ms,
                        ),
                    )

                if isinstance(cached_run_result, NoRunResult):
                    try:
                        self._run_cache.confirm_execution(
                            self._node,
                            cached_run_result.request_id,
                            failed_to_clone=cached_run_result.failed_to_clone,
                            execution_runtime_ms=elapsed_ms,
                        )
                    except Exception as e:
                        events.fire_warn_event_with_cache_bypass(
                            "Error confirming execution for test '{}': {}",
                            self._node.unique_id,
                            str(e),
                        )
                elif cached_run_result is None:
                    # The CTAS executed without state tracking; invalidate the failures
                    # table's cached metadata so the follow-up count query reports its
                    # actual freshness instead of the pre-CTAS timestamp
                    self._run_cache.on_state_request_failed(self._node)
                return result

        except SqlglotError as e:
            events.fire_warn_event_with_cache_bypass(
                "Failed to parse SQL for test '{}': {}",
                self._node.unique_id,
                str(e),
            )
        except Exception as e:
            events.fire_warn_event_with_cache_bypass(
                "Unexpected error processing dbt State response for test '{}': {}",
                self._node.unique_id,
                str(e),
            )
        return self._adapter.execute(sql, *args, **kwargs)

    def drop_relation(self, relation: BaseRelation) -> None:
        if relation.type == RelationType.Table and (
            self._node.schema.lower(),
            self._node.identifier.lower(),
        ) == (
            (relation.schema or "").lower(),
            (relation.identifier or "").lower(),
        ):
            # Postpone deletion of the test relation until after we check the cache response for the
            # test's CTAS statement which follows this call
            self._relation_to_drop = relation
        else:
            self._adapter.drop_relation(relation)
