from __future__ import annotations

import typing as t
import uuid
from dataclasses import dataclass
from datetime import datetime
from time import perf_counter

import grpc
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ModelNode,
    SeedNode,
    SingularTestNode,
    SnapshotNode,
)
from query_cache_common.models import shared_models
from query_cache_common.models.services import (
    client_telemetry_service_models,
    clone_service_models,
    sql_service_models,
)
from sqlglot.errors import SqlglotError

from dbt_state import events

if t.TYPE_CHECKING:
    from dbt.contracts.graph.nodes import ManifestNode

    from dbt_state._typing import (
        ModelOrSnapshotNode,
        ModelOrSnapshotOrTestNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )
    from dbt_state.adapters import BaseAdapterExtension
    from dbt_state.adapters.common import ViewTraversalResult
    from dbt_state.config import RunCacheConfig
    from dbt_state.dev_cloner import DevCloner
    from dbt_state.dispatcher import TelemetryDispatcher
    from dbt_state.freshness import Freshness
    from dbt_state.grpc.client import QueryCacheGrpcClient
    from dbt_state.prefetch import MetadataPrefetcher
    from dbt_state.request_builder import RequestBuilder


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


class StateRequestSubmitter:
    """Builds and submits SQL, values and clone requests to the query cache service.

    Owns the submit flow (including the speculative path), the telemetry emitted while preparing
    a request, and the warning logged when preparation fails. Decision IDs returned by the
    service are handed to ``record_decision_id``.
    """

    def __init__(
        self,
        query_cache_client: QueryCacheGrpcClient,
        prefetcher: MetadataPrefetcher,
        request_builder: RequestBuilder,
        adapter_ext: BaseAdapterExtension,
        freshness: Freshness,
        telemetry_dispatcher: TelemetryDispatcher,
        run_cache_config: RunCacheConfig,
        record_decision_id: t.Callable[[ManifestNode, t.Optional[str]], None],
    ) -> None:
        self._query_cache_client = query_cache_client
        self._prefetcher = prefetcher
        self._request_builder = request_builder
        self._adapter_ext = adapter_ext
        self._freshness = freshness
        self._telemetry_dispatcher = telemetry_dispatcher
        self._run_cache_config = run_cache_config
        self._record_decision_id = record_decision_id

    @property
    def _is_write_only(self) -> bool:
        return self._run_cache_config.cache_mode.is_write_only

    def submit_sql(
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
        """Submit an enriched SQL request for a model, snapshot or test node.

        Args:
            node: The node being executed.
            sql: SQL to submit instead of the node's compiled code (e.g. a data test query).
            execution_type: Overrides the execution type derived from the node.
            microbatch_window: The (start, end) event-time window of a microbatch run, if any.

        Returns:
            The service response, a ``CacheBypassedResponse`` in write-only mode or for a
            speculative untracked-execute verdict, or None if the request could not be prepared.
        """
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

                # Non-table references (e.g. Snowflake Stages) were skipped during traversal, so
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

            use_speculative = not self._is_write_only and not self._prefetcher.is_prefetch_ready()
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

            if self._is_write_only:
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
            self._record_decision_id(node, response.execution_decision_id)

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

    def submit_values(
        self,
        node: SeedNode,
    ) -> t.Union[
        sql_service_models.ReadyToExecuteResponse,
        sql_service_models.SkipExecutionResponse,
        clone_service_models.ReadyToCloneResponse,
        CacheBypassedResponse,
        None,
    ]:
        """Submit a values request for a seed node.

        Returns:
            The service response, a ``CacheBypassedResponse`` in write-only mode, or None if the
            request could not be prepared.
        """
        request_id = uuid.uuid4().hex
        try:
            request = self._request_builder.build_submit_values_request(node)

            if self._is_write_only:
                return CacheBypassedResponse(request, node)

            response = self._query_cache_client.submit_values(request, request_id)
            self._record_decision_id(node, response.execution_decision_id)
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

    def submit_clone(
        self, node: ModelOrSnapshotNode, dev_cloner: DevCloner
    ) -> t.Optional[
        t.Union[
            clone_service_models.ReadyToCloneResponse, clone_service_models.UnableToCloneResponse
        ]
    ]:
        """Register a dev clone of ``node`` with the service.

        Returns:
            The service's clone verdict, or None if no clone source exists for the node.
        """
        result = dev_cloner.get_clone_source(node)
        if not result:
            return None
        clone_source, clone_source_table_type = result
        clone_request = self._request_builder.build_clone_request(
            node, clone_source, clone_source_table_type
        )
        return self._query_cache_client.register_clone(clone_request)

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
            self._record_decision_id(node, response.execution_decision_id)
            return response
        if isinstance(response, sql_service_models.ReadyToExecuteUntrackedResponse):
            return response
        # Undecided, or any unexpected response type: block on the prefetch and resubmit.
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
