from __future__ import annotations

import threading
import typing as t
import uuid
from dataclasses import dataclass, replace
from datetime import datetime
from functools import cached_property
from time import perf_counter

import agate
import grpc
import humanize
from dbt.adapters.base.relation import BaseRelation, RelationType
from sqlglot import exp, parse_one
from sqlglot.errors import SqlglotError

try:
    from dbt.artifacts.resources.v1.config import TestConfig
    from dbt.artifacts.resources.v1.model import ModelConfig
    from dbt.artifacts.resources.v1.snapshot import SnapshotConfig
except ImportError:
    from dbt.contracts.graph.model_config import (  # type: ignore[no-redef]
        NodeConfig as ModelConfig,
    )
    from dbt.contracts.graph.model_config import (
        SnapshotConfig,
        TestConfig,
    )

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
    clone_service_models,
    execution_service_models,
    sql_service_models,
)
from query_cache_common.models.services.explain_service_models import ExplainMessageEntry

from dbt_state import events
from dbt_state._typing import MODEL_OR_SNAPSHOT_OR_TEST_NODE
from dbt_state.adapters import BaseAdapterExtension, create_adapter_extension
from dbt_state.adapters.common import ViewTraversalResult
from dbt_state.config import RunCacheConfig
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
from dbt_state.utils import (
    get_dbt_command_name,
    is_table,
    is_view,
)

# Feature-detect RunStatus.Reused. Older dbt versions do not define it.
_RUN_STATUS_REUSED = getattr(RunStatus, "Reused", None)

if t.TYPE_CHECKING:
    from dbt.adapters.base import BaseRelation
    from dbt.adapters.sql import SQLAdapter

    from dbt_state._typing import (
        ModelOrSnapshotNode,
        ModelOrSnapshotOrSeedNode,
        ModelOrSnapshotOrTestNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )

RequestId = str
FailedToClone = bool


class _RunResultWithStateDecisionId(t.Protocol):
    state_decision_id: t.Optional[str]


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

        self._total_cache_hits: int = 0
        self._total_time_saved_ms: int = 0
        self._reused_status_warning_emitted: bool = False
        events.register_callback("run-cache", self.on_event)

        self._run_result = client_telemetry_service_models.ClientResult.SUCCESS

        # map of node.unique_id -> CacheBypassedResponse
        # collected in _process_query_cache_response and published as write-only executions
        self._cache_bypass_responses: t.Dict[str, CacheBypassedResponse] = {}
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

    def confirm_execution(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        request_id: RequestId,
        failed_to_clone: bool = False,
        execution_runtime_ms: t.Optional[int] = None,
    ) -> t.Optional[RequestId]:
        """Confirms the execution of a model node with the query cache service.

        Args:
            node: The model node that was executed.
            request_id: The request ID returned from the query cache for the given model's execution.
            failed_to_clone: Whether the model failed to be cloned during execution.

        Returns:
            The execution ID, which may differ from the input request_id for clones
            (where a new execution record is created). Returns None if confirmation was skipped.
        """
        target_table_type, last_modified_epoch = (
            self._freshness.get_target_table_type_and_last_modified_epoch(node)
        )
        if last_modified_epoch is None:
            events.fire_debug_event(
                "Skipping confirmation for node {} due to missing last modified epoch",
                node.unique_id,
            )
            return None

        confirmation_request = execution_service_models.ConfirmExecutionRequest(
            request_id=request_id,
            last_modified_epoch=last_modified_epoch,
            failed_to_clone=failed_to_clone,
            table_type=target_table_type,
            execution_runtime_ms=execution_runtime_ms,
            labels=self._request_builder.get_request_labels(node),
        )
        response = self._query_cache_client.confirm_execution(confirmation_request)
        if response.success:
            events.fire_debug_event(
                "Confirmed execution for node {}, execution_id: {}",
                node.unique_id,
                response.execution_id,
            )
            self._decision_logger.log_confirm_execution(node.name, response.execution_id)
            return response.execution_id
        events.fire_debug_event(
            "Execution confirmation failed for node {}, request_id: {}",
            node.unique_id,
            request_id,
        )
        return None

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
        self._prefetcher.await_prefetch_last_modified()
        table_names = [info.name for info in request.tables]
        if not table_names:
            return request
        overrides = (
            self._freshness.resolve_dbt_source_freshness_overrides(node)
            if isinstance(node, ModelNode)
            else {}
        )
        epochs = self._adapter_ext.get_last_modified_epoch(table_names, table_overrides=overrides)
        refreshed_tables = [
            replace(info, last_modified_epoch=epochs.get(info.name, info.last_modified_epoch))
            for info in request.tables
        ]
        return replace(request, tables=refreshed_tables)

    def on_run_result(self, node: ModelOrSnapshotOrSeedNode, result: RunResult) -> None:
        if not (bypass_response := self._cache_bypass_responses.get(node.unique_id)):
            return

        target_table_type, last_modified_epoch = (
            self._freshness.get_target_table_type_and_last_modified_epoch(node)
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
        if node.unique_id in self._cache_bypass_responses:
            # write-only executions refresh the cache in on_run_result() instead
            return

        try:
            self._adapter_ext.clear_cache([self._node_resolution.node_to_table(node)])
        except Exception as e:
            events.fire_debug_event(
                "Failed to clear cached metadata for node {}: {}", node.unique_id, str(e)
            )

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
                        labels=self._request_builder.get_request_labels(node),
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
        context, context_config, hook_ctx = self._hooks.handle_pre_hooks(should_run_hooks, node)

        # Track the confirmed request ID for post-hook metadata updates.
        # For clones, this may differ from query_cache_response.request_id.
        confirmed_execution_id: t.Optional[RequestId] = None

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
                current_last_modified_epoch = self._freshness.get_last_modified_epoch(
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
                # drop the clone target before attempting the clone, otherwise we can run into a problem where we try to clone
                # a table on top of a view
                if (
                    existing_relation := self._adapter_ext.fqn_to_cached_relation(
                        query_cache_response.clone_target
                    )
                ) and existing_relation.type != RelationType.Table:
                    self._adapter.drop_relation(existing_relation)

                if self._adapter_ext.IMPLEMENTS_CUSTOM_CLONE:
                    self._adapter_ext.clone(
                        query_cache_response.clone_sqls,
                        query_cache_response.clone_source,
                        query_cache_response.clone_target,
                    )
                else:
                    for sql in query_cache_response.clone_sqls:
                        self._adapter.execute(sql)
            self._adapter_ext.commit_if_open()
            # when we clone a table, we put it in the relation cache so that the remainder of the
            # invocation knows it exists without hitting the db
            self._adapter_ext.cache_node_relation(node)
            confirmed_execution_id = self.confirm_execution(node, query_cache_response.request_id)
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
            # Skips reuse an existing execution; clones only have one once confirmed.
            execution_id = (
                query_cache_response.execution_id
                if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse)
                else confirmed_execution_id
            )
            self._hooks.handle_post_hooks(
                should_run_hooks,
                node,
                query_cache_response,
                context,
                context_config,
                hook_ctx,
                execution_id,
            )

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
        self._adapter_ext.commit_if_open()
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
            self._record_execution_decision_id(node, response.execution_decision_id)
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
            self._prefetcher.start_prefetch_last_modified()

            # Resolve inputs and run the (prefetch-independent) view traversal up front. The
            # traversal blocks on view-definition fetches while the async last-modified prefetch
            # runs concurrently, so deferring the speculative decision until afterwards lets us
            # take the accurate non-speculative path for free whenever the prefetch completed
            # during the traversal window.
            resolved_sql = sql or node.compiled_code or ""
            if not resolved_sql:
                raise RuntimeError(f"Model node '{node.unique_id}' must be compiled")
            resolved_execution_type = execution_type or shared_models.ModelExecutionType(
                self._request_builder.node_execution_type(node)
            )
            traversal_result: t.Optional[ViewTraversalResult] = None
            view_traversal_duration_ms: t.Optional[int] = None
            if resolved_execution_type != shared_models.ModelExecutionType.VIEW:
                view_traversal_start = perf_counter()
                terminal_fqns = (
                    set(self._freshness.resolve_dbt_source_freshness_overrides(node))
                    if isinstance(node, ModelNode)
                    else set()
                )
                # a freshness override (loaded_at_field / loaded_at_query) determines this relation's
                # last_modified, so record it as a dependency but don't expand it into its underlying tables
                traversal_result = self._adapter_ext.traverse_view_definitions(
                    resolved_sql, terminal_fqns
                )
                view_traversal_duration_ms = int((perf_counter() - view_traversal_start) * 1000)

                # Non-table references (e.g. Snowfalke Stages) were skipped during traversal, so
                # nothing can check their freshness. A source with a freshness override is never expanded,
                # so reaching one here means no override covers it. Run without state rather than risk
                # reusing a model whose upstream data changed
                if traversal_result.unsupported_references:
                    events.fire_warn_event_with_cache_bypass(
                        "Model {} reads from {}, table reference(s) that dbt State does not currently support,"
                        " so they cannot be checked for updates."
                        " To let dbt State check for updates, read them through a view declared as a dbt source"
                        " with loaded_at_field or loaded_at_query. See {}",
                        node.unique_id,
                        ", ".join(sorted(traversal_result.unsupported_references)),
                        "https://docs.getdbt.com/reference/resource-configs/freshness?version=1#using-loaded_at_query",
                    )
                    return None

            use_speculative = not self.is_write_only and not self._prefetcher.is_prefetch_ready()
            if not use_speculative:
                self._prefetcher.await_prefetch_last_modified()

            request, last_modified_duration_ms = (
                self._request_builder.build_submit_enriched_sql_request(
                    node,
                    resolved_sql,
                    resolved_execution_type,
                    traversal_result=traversal_result,
                    microbatch_window=microbatch_window,
                    speculative=use_speculative,
                )
            )
            request_end_time = perf_counter()
            duration = request_end_time - request_start_time

            self._emit_enriched_sql_prepared_telemetry(
                request_id,
                duration,
                target_table_fqn=node.relation_name,
                labels=self._request_builder.get_request_labels(node),
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
                self._prefetcher.await_prefetch_last_modified()
                request, _ = self._request_builder.build_submit_enriched_sql_request(
                    node,
                    resolved_sql,
                    resolved_execution_type,
                    traversal_result=traversal_result,
                    microbatch_window=microbatch_window,
                    speculative=False,
                )

            response = self._query_cache_client.submit_sql(request, request_id)
            self._record_execution_decision_id(node, response.execution_decision_id)

            return response

        except Exception as e:
            request_end_time = perf_counter()
            self._log_submit_sql_error(e, node)
            duration = request_end_time - request_start_time
            self._emit_enriched_sql_prepared_telemetry(
                request_id,
                duration=duration,
                target_table_fqn=node.relation_name,
                labels=self._request_builder.get_request_labels(node),
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
            request = self._request_builder.build_submit_values_request(node)

            if self.is_write_only:
                return CacheBypassedResponse(request, node)

            response = self._query_cache_client.submit_values(request, request_id)
            self._record_execution_decision_id(node, response.execution_decision_id)
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

    @staticmethod
    def _log_submit_sql_error(e: Exception, node: ModelOrSnapshotOrTestNode) -> None:
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
        clone_request = self._request_builder.build_clone_request(
            node, clone_source, clone_source_table_type
        )
        return self._query_cache_client.register_clone(clone_request)

    def _record_cache_hit(
        self,
        response: t.Union[
            sql_service_models.SkipExecutionResponse, clone_service_models.ReadyToCloneResponse
        ],
    ) -> None:
        self._total_cache_hits += 1
        self._total_time_saved_ms += response.execution_runtime_ms or 0

    def resolve_state_deferred_relations(self) -> None:
        """Trigger the one-time state-based deferred-relation resolve."""
        _ = self._node_resolution.state_deferred_fqn_by_unique_id

    def _cache_hit_run_status(self) -> RunStatus:
        """Return the ``RunStatus`` to use for cache-hit results (no-op or clone).

        Return ``RunStatus.Reused`` when enabled and supported. Otherwise return
        ``RunStatus.Success``. If reused status is enabled but unsupported, emit
        one warning before returning ``RunStatus.Success``.
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

        When ``emit_reused_status`` is enabled and supported, emit the new status with a
        Fusion-style message describing the clone. Otherwise use the legacy
        ``Success`` + "CLONE" representation.
        """
        status = self._cache_hit_run_status()
        if status is _RUN_STATUS_REUSED:
            suffix = " within tolerance" if is_stale else ""
            return status, "Cloned from other environment" + suffix
        legacy_suffix = " (within tolerance)" if is_stale else ""
        return status, "CLONE" + legacy_suffix

    def _no_op_status_and_message(
        self,
        is_stale: bool,
        node_config: t.Union[ModelConfig, SnapshotConfig, TestConfig],
    ) -> t.Tuple[RunStatus, str]:
        """Return (status, message) for cache-hit no-op results.

        When ``emit_reused_status`` is enabled and supported, emit the new status with a
        Fusion-style message describing why the node was reused. Otherwise use
        the legacy ``Success`` + "NO-OP" representation.
        """
        status = self._cache_hit_run_status()
        if status is not _RUN_STATUS_REUSED:
            freshness_suffix = " (within tolerance)" if is_stale else ""
            return status, NO_OP_STATUS + freshness_suffix
        if is_stale:
            tolerance_seconds = self._run_cache_config.resolve_freshness_tolerance(node_config)
            message = (
                f"New changes detected within lag tolerance of "
                f"{humanize.naturaldelta(tolerance_seconds)}"
            )
        else:
            message = "No new changes"
        return status, message

    @property
    def _adapter(self) -> SQLAdapter:
        return self._adapter_ext.adapter

    @property
    def dialect(self) -> str:
        return self._node_resolution.dialect

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
                    query_cache_response = self._run_cache._submit_sql_request(  # noqa: SLF001
                        self._node, sql=sql, execution_type=execution_type
                    )
                    cached_run_result = self._run_cache._process_query_cache_response(  # noqa: SLF001
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
                    self._run_cache._publish_write_only_execution(  # noqa: SLF001
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
