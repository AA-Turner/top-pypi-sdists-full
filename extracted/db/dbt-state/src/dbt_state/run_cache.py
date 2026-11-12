from __future__ import annotations

import threading
import typing as t
from datetime import datetime
from functools import cached_property
from time import perf_counter

import agate
from dbt.adapters.base.relation import BaseRelation, RelationType
from sqlglot import exp, parse_one
from sqlglot.errors import SqlglotError

try:
    from dbt.adapters.contracts.connection import AdapterResponse
    from dbt.artifacts.resources.v1.components import DeferRelation
except ImportError:
    from dbt.contracts.connection import AdapterResponse  # type: ignore
    from dbt.contracts.graph.nodes import DeferRelation  # type: ignore[no-redef]

from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ManifestNode,
    ManifestSQLNode,
    ModelNode,
    SeedNode,
    SingularTestNode,
    SnapshotNode,
)
from dbt.contracts.results import RunResult, RunStatus

try:
    from dbt_common.clients import agate_helper
except ImportError:
    from dbt.clients import agate_helper  # type: ignore

from query_cache_common.constants import NO_OP_STATUS, SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS
from query_cache_common.models import shared_models
from query_cache_common.models.services import (
    client_telemetry_service_models,
    execution_service_models,
    sql_service_models,
)

from dbt_state import events
from dbt_state._typing import MODEL_OR_SNAPSHOT_OR_TEST_NODE
from dbt_state.adapters import BaseAdapterExtension, create_adapter_extension
from dbt_state.config import RunCacheConfig
from dbt_state.decision_executor import DecisionExecutor, NoRunResult
from dbt_state.decision_logger import BaseDecisionLogger, create_decision_logger
from dbt_state.dev_cloner import DevCloner
from dbt_state.dispatcher import TelemetryDispatcher
from dbt_state.freshness import Freshness
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.hooks import Hooks
from dbt_state.node_resolution import NodeResolution
from dbt_state.prefetch import MetadataPrefetcher
from dbt_state.profiles import Profiles
from dbt_state.relation import DeferredRelationResolver
from dbt_state.request_builder import RequestBuilder
from dbt_state.session import SessionManager
from dbt_state.submitter import CacheBypassedResponse, StateRequestSubmitter
from dbt_state.utils import (
    get_dbt_command_name,
    is_table,
    is_view,
)

if t.TYPE_CHECKING:
    from dbt.adapters.base import BaseRelation
    from dbt.adapters.sql import SQLAdapter

    from dbt_state._typing import (
        ModelOrSnapshotNode,
        ModelOrSnapshotOrTestNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )

RequestId = str
FailedToClone = bool


class _RunResultWithStateDecisionId(t.Protocol):
    state_decision_id: t.Optional[str]


_HASH_READ_CHUNK_SIZE = 64 * 1024


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
        self._adapter_ext = adapter_ext
        self._config = config
        self._manifest = manifest
        self._decision_logger = decision_logger
        self._run_cache_config = run_cache_config
        self._telemetry_dispatcher = telemetry_dispatcher
        self._session_manager = session_manager
        self._node_resolution = NodeResolution(
            manifest=manifest,
            adapter_ext=adapter_ext,
            deferred_relation_resolver=deferred_relation_resolver,
            profiles=profiles,
            config=config,
            run_cache_config=run_cache_config,
            query_cache_client=query_cache_client,
        )

        self._freshness = Freshness(
            adapter_ext=adapter_ext,
            node_resolution=self._node_resolution,
            manifest=manifest,
            config=config,
        )

        self._prefetcher = MetadataPrefetcher(
            adapter_ext=adapter_ext,
            node_resolution=self._node_resolution,
            freshness=self._freshness,
            manifest=manifest,
            config=config,
        )

        self._request_builder = RequestBuilder(
            adapter_ext=adapter_ext,
            node_resolution=self._node_resolution,
            freshness=self._freshness,
            prefetcher=self._prefetcher,
            profiles=profiles,
            manifest=manifest,
            config=config,
            run_cache_config=run_cache_config,
        )

        self._submitter = StateRequestSubmitter(
            query_cache_client=query_cache_client,
            prefetcher=self._prefetcher,
            request_builder=self._request_builder,
            adapter_ext=adapter_ext,
            freshness=self._freshness,
            telemetry_dispatcher=telemetry_dispatcher,
            run_cache_config=run_cache_config,
            record_decision_id=self._record_execution_decision_id,
        )

        self._hooks = Hooks(
            adapter_ext=adapter_ext,
            node_resolution=self._node_resolution,
            freshness=self._freshness,
            query_cache_client=query_cache_client,
            run_cache_config=run_cache_config,
            node_execution_type=self._request_builder.node_execution_type,
            config=config,
            manifest=manifest,
        )

        self._executor = DecisionExecutor(
            adapter_ext=adapter_ext,
            query_cache_client=query_cache_client,
            run_cache_config=run_cache_config,
            config=config,
            manifest=manifest,
            node_resolution=self._node_resolution,
            freshness=self._freshness,
            prefetcher=self._prefetcher,
            request_builder=self._request_builder,
            hooks=self._hooks,
            decision_logger=decision_logger,
            dev_cloner=dev_cloner,
        )
        events.register_callback("run-cache", self.on_event)

        self._run_result = client_telemetry_service_models.ClientResult.SUCCESS

        self._execution_decision_ids: t.Dict[str, str] = {}
        self._execution_decision_ids_lock = threading.Lock()

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
            adaptive_metadata_fetch=run_cache_config.adaptive_metadata_fetch,
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
            query_cache_response = self._submitter.submit_values(node)
        elif (
            isinstance(node, (ModelNode, SnapshotNode))
            and node.language == "sql"
            and (
                is_table(node) or (is_view(node) and self._adapter_ext.supports_view_last_modified)
            )
        ):
            query_cache_response = self._submitter.submit_sql(
                node, microbatch_window=microbatch_window
            )
        else:
            return None
        return self._executor.act(node, query_cache_response)

    def on_compile(self, node: ManifestSQLNode) -> None:
        """Invoked during the compilation of a model node.

        Automatically clones selected incremental models when appropriate, except
        during dbt compile because compile must not create or mutate relations.

        Args:
            node: The model node being compiled.
        """
        if self._is_dbt_compile_command:
            # we dont need to trigger off all the metadata prefetches on `dbt compile`
            # or pre-emptively make dev clones of deferred relations
            # the metadata prefetches are used for making cache decisions, but `dbt compile`
            # doesnt make cache decisions
            return

        try:
            self._prefetcher.start_prefetch_last_modified()
        except Exception as e:
            events.fire_warn_event("Failed to prefetch last modified timestamps: {}", str(e))

        if isinstance(
            node, MODEL_OR_SNAPSHOT_OR_TEST_NODE
        ) and self._run_cache_config.resolve_compare_selected_columns(node.config):
            try:
                self._prefetcher.start_prefetch_schemas()
            except Exception as e:
                events.fire_warn_event("Failed to prefetch schemas: {}", str(e))

        if isinstance(node, (ModelNode, SnapshotNode)):
            self._try_clone(node)

    @cached_property
    def _is_dbt_compile_command(self) -> bool:
        """Whether the top-level dbt command is compile.

        dbt also invokes model compile hooks while running commands like run and build.
        Those commands can still clone; only dbt compile must avoid relation mutations.
        """
        return get_dbt_command_name(getattr(self._config, "args", None)) == "compile"

    def get_defer_relation(self, node: ManifestNode) -> t.Optional[DeferRelation]:
        """Returns a DeferRelation for the given node if it should be deferred.

        Delegates to `NodeResolution.get_defer_relation`.

        Args:
            node: The manifest node to potentially defer.

        Returns:
            A DeferRelation if the node should be deferred, otherwise None.
        """
        return self._node_resolution.get_defer_relation(node)

    def cache_compiled_view_sql(self, node: ManifestSQLNode) -> None:
        """Pre-populate the view definition cache from a compiled dbt model node.

        Only caches plain view models (not materialized_view, ephemeral, etc.) or an audit
        relation of a data test with storage failures stored as a view that have
        compiled SQL available. This avoids expensive database round-trips for views whose
        SQL is already known from dbt compilation.

        Args:
            node: The compiled manifest node to potentially cache.
        """
        is_data_test_with_failure_view = (
            isinstance(node, (GenericTestNode, SingularTestNode))
            and getattr(node.config, "store_failures", None)
            and getattr(node.config, "store_failures_as", None) == "view"
        )
        if (
            isinstance(node, ModelNode)
            and (node.get_materialization() or "view") == "view"
            and node.compiled_code
        ) or (
            is_data_test_with_failure_view
            # Skip caching the definition when the test sets `limit`. We take the definition
            # from node.compiled_code, but `limit` is not included in the node's compiled code.
            # dbt adds the limit only at materialization, when the view is actually created.
            # This means compiled_code wouldn't match the built view, so the data test count
            # query that reads this cached definition would be using a view body that does
            # not match what was materialized.
            and getattr(node.config, "limit", None) is None
            and node.compiled_code
        ):
            table = self._node_resolution.node_to_table(node)
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

    def begin_on_run_end(self) -> None:
        self._hooks.begin_on_run_end()

    def update_metadata_after_on_run_end(self) -> None:
        self._hooks.update_metadata_after_on_run_end()

    def before_on_run_end_statement(self, sql: str) -> t.Set[str]:
        return self._hooks.before_on_run_end_statement(sql)

    def after_on_run_end_statement(self, unique_ids: t.Iterable[str]) -> None:
        self._hooks.after_on_run_end_statement(unique_ids)

    def prewarm_connections(self) -> None:
        self._adapter_ext.prewarm_connections()

    def close(self) -> None:
        self._adapter_ext.close()

    def attach_state_decision_id(self, node: ManifestNode, result: RunResult) -> None:
        """Attach the node's latest State decision ID to its structured dbt result.

        Newer dbt Core versions include ``RunResult.state_decision_id`` in the per-node
        ``NodeFinished`` event. Feature-detect the field so older supported versions continue
        without emitting it.
        """
        with self._execution_decision_ids_lock:
            execution_decision_id = self._execution_decision_ids.get(node.unique_id)
        if execution_decision_id and hasattr(result, "state_decision_id"):
            result_with_state_decision_id = t.cast(_RunResultWithStateDecisionId, result)
            result_with_state_decision_id.state_decision_id = execution_decision_id

    def _record_execution_decision_id(
        self,
        node: ManifestNode,
        execution_decision_id: t.Optional[str],
    ) -> None:
        if not execution_decision_id:
            return
        self._decision_logger.log_execution_decision_id(
            node_name=node.name, execution_decision_id=execution_decision_id
        )
        with self._execution_decision_ids_lock:
            self._execution_decision_ids[node.unique_id] = execution_decision_id

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
        self._executor.invalidate(node)

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
        query_cache_response = self._submitter.submit_sql(
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
                    self._executor.publish_write_only_execution(
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
                        labels=self._request_builder.get_request_labels(node),
                    )
                    self._query_cache_client.confirm_execution(confirmation_request)
                    events.fire_debug_event(
                        "Confirmed execution for test {}, request_id {}", node.unique_id, request_id
                    )
            return adapter_response, agate_table
        if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
            events.fire_debug_event("Received skip execution response for node {}", node.name)
            self._executor.record_cache_hit(query_cache_response)
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

    def _try_clone(self, node: ModelOrSnapshotNode) -> bool:
        if self._dev_cloner is None or self.is_write_only:
            return False
        clone_response = self._submitter.submit_clone(node, self._dev_cloner)
        if clone_response is None:
            return False

        return self._executor.act_dev_clone(node, clone_response)

    def resolve_state_deferred_relations(self) -> None:
        """Trigger the one-time state-based deferred-relation resolve."""
        _ = self._node_resolution.state_deferred_fqn_by_unique_id

    @property
    def _adapter(self) -> SQLAdapter:
        return self._adapter_ext.adapter

    def run_node(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        act_result: t.Union[RunResult, NoRunResult, None],
        execute: t.Callable[[], RunResult],
        should_confirm: t.Callable[[RunResult], bool],
    ) -> RunResult:
        """Finish a node's execution given what ``on_execute`` returned for it."""
        return self._executor.run(node, act_result, execute, should_confirm)

    def cache_hit_run_status(self) -> RunStatus:
        """Return the ``RunStatus`` to use for cache-hit results (no-op or clone)."""
        return self._executor.cache_hit_run_status()

    def log_node_start(self, node: ManifestNode) -> None:
        """Start collecting decision logging information about a node."""
        self._decision_logger.log_node_start(node)

    def log_deferral(self, node_name: str, relation_name: str, deferred_to_fqn: str) -> None:
        """Log that a relation was deferred to a table from another environment."""
        self._decision_logger.log_deferral(node_name, relation_name, deferred_to_fqn)

    @property
    def enable_data_tests(self) -> bool:
        """Whether data tests go through the cache."""
        return self._run_cache_config.enable_data_tests

    @property
    def dialect(self) -> str:
        return self._node_resolution.dialect

    @property
    def run_cache_config(self) -> RunCacheConfig:
        return self._run_cache_config

    @property
    def total_cache_hits(self) -> int:
        return self._executor.total_cache_hits

    @property
    def total_time_saved_ms(self) -> int:
        return self._executor.total_time_saved_ms

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
        self._adapter = run_cache._adapter  # noqa: SLF001
        self._adapter_ext = self._run_cache._adapter_ext  # noqa: SLF001
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
                return self._run_cache._on_data_test_query(  # noqa: SLF001
                    self._node,
                    sql,
                    lambda: self._adapter.execute(sql, *args, **kwargs),
                )
            if isinstance(parsed_test_sql, exp.Create) and parsed_test_sql.kind in (
                "TABLE",
                "VIEW",
            ):
                # Handle the CTAS statement which creates a table or the CREATE VIEW AS SELECT which creates a view
                # with data test failures
                cached_run_result = None
                query_cache_response = None
                execution_type = (
                    shared_models.ModelExecutionType.VIEW
                    if parsed_test_sql.kind == "VIEW"
                    else shared_models.ModelExecutionType.FULL
                )
                materialization_kind = (
                    RelationType.View.value
                    if parsed_test_sql.kind == "VIEW"
                    else RelationType.Table.value
                )
                try:
                    query_cache_response = self._run_cache._submitter.submit_sql(  # noqa: SLF001
                        self._node, sql=sql, execution_type=execution_type
                    )
                    cached_run_result = self._run_cache._executor.act(  # noqa: SLF001
                        self._node, query_cache_response
                    )
                    if isinstance(cached_run_result, RunResult):
                        # We got a cache hit for the CTAS statement
                        explained_decision = getattr(
                            query_cache_response, "explained_decision", None
                        )
                        decision = (
                            explained_decision.decision
                            if explained_decision
                            else shared_models.SubmitSQLResultType.SKIP_EXECUTION
                        )
                        description = (
                            explained_decision.decision_description if explained_decision else ""
                        )
                        self._run_cache._decision_logger.log_stored_failures(  # noqa: SLF001
                            self._node.name,
                            materialization_kind,
                            decision,
                            description,
                        )
                        self._adapter.commit_if_has_connection()
                        return AdapterResponse(_message=NO_OP_STATUS), agate.Table.from_object([])  # ty: ignore[unresolved-attribute]
                except Exception as e:
                    events.fire_warn_event_with_cache_bypass(
                        "Error processing dbt State response for test '{}': {}",
                        self._node.unique_id,
                        str(e),
                    )
                explained_decision = getattr(query_cache_response, "explained_decision", None)
                decision = (
                    explained_decision.decision
                    if explained_decision
                    else shared_models.SubmitSQLResultType.READY_TO_EXECUTE
                )
                description = explained_decision.decision_description if explained_decision else ""
                self._run_cache._decision_logger.log_stored_failures(  # noqa: SLF001
                    self._node.name,
                    materialization_kind,
                    decision,
                    description,
                )
                execution_start_ts = perf_counter()
                if self._relation_to_drop:
                    # Execute the postponed drop
                    self._adapter.drop_relation(self._relation_to_drop)
                result = self._adapter.execute(sql, *args, **kwargs)
                elapsed_ms = int((perf_counter() - execution_start_ts) * 1000)
                self._adapter_ext.cache_node_relation(
                    self._node,
                    relation_type=RelationType.View
                    if parsed_test_sql.kind == "VIEW"
                    else RelationType.Table,
                )

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
                        self._run_cache._freshness.get_target_table_type_and_last_modified_epoch(  # noqa: SLF001
                            self._node
                        )
                    )
                    self._run_cache._executor.publish_write_only_execution(  # noqa: SLF001
                        bypass_response=query_cache_response,
                        outcome=execution_service_models.ExecutionOutcome(
                            last_modified_epoch=last_modified_epoch,
                            table_type=table_type,
                            execution_runtime_ms=elapsed_ms,
                        ),
                    )

                if isinstance(cached_run_result, NoRunResult):
                    try:
                        self._run_cache._executor.confirm_execution(  # noqa: SLF001
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
        if relation.type in (RelationType.Table, RelationType.View) and (
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
