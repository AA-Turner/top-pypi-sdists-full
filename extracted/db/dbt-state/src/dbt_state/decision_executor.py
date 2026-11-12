from __future__ import annotations

import typing as t
from dataclasses import dataclass, replace
from time import perf_counter

import humanize
from dbt.adapters.base.relation import RelationType
from dbt.contracts.graph.nodes import ModelNode
from dbt.contracts.results import RunResult, RunStatus
from query_cache_common.constants import NO_OP_STATUS
from query_cache_common.models.services import (
    clone_service_models,
    execution_service_models,
    sql_service_models,
)
from query_cache_common.models.services.explain_service_models import ExplainMessageEntry
from sqlglot import exp

from dbt_state import events
from dbt_state.submitter import CacheBypassedResponse

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

# Feature-detect RunStatus.Reused. Older dbt versions do not define it.
_RUN_STATUS_REUSED = getattr(RunStatus, "Reused", None)

if t.TYPE_CHECKING:
    from dbt.adapters.sql import SQLAdapter
    from dbt.config.runtime import RuntimeConfig
    from dbt.contracts.graph.manifest import Manifest

    from dbt_state._typing import (
        ModelOrSnapshotNode,
        ModelOrSnapshotOrSeedNode,
        ModelOrSnapshotOrTestOrSeedNode,
    )
    from dbt_state.adapters import BaseAdapterExtension
    from dbt_state.config import RunCacheConfig
    from dbt_state.decision_logger import BaseDecisionLogger
    from dbt_state.dev_cloner import DevCloner
    from dbt_state.freshness import Freshness
    from dbt_state.grpc.client import QueryCacheGrpcClient
    from dbt_state.hooks import Hooks
    from dbt_state.node_resolution import NodeResolution
    from dbt_state.prefetch import MetadataPrefetcher
    from dbt_state.request_builder import RequestBuilder

RequestId = str


@dataclass
class NoRunResult:
    request_id: str
    """The unique identifier for the execution request."""
    failed_to_clone: bool


class DecisionExecutor:
    """Acts on the query cache server's decision for a node and records what happened.

    Owns the "act" and "record" halves of the decide -> act -> record loop:

    - ``act`` turns a server response into a ``RunResult`` (reuse or clone, including hooks)
      or tells the caller to execute the node normally.
    - ``confirm_execution`` / ``record_run_result`` / ``publish_write_only_execution`` report
      the outcome of an execution back to the server.
    - ``invalidate`` drops locally cached metadata for a node whose execution won't be confirmed.

    It also owns the state those steps share: the untracked-execution responses awaiting
    their outcome, the cache-hit counters and the reused-status warning flag.
    """

    def __init__(
        self,
        *,
        adapter_ext: BaseAdapterExtension,
        query_cache_client: QueryCacheGrpcClient,
        run_cache_config: RunCacheConfig,
        config: RuntimeConfig,
        manifest: Manifest,
        node_resolution: NodeResolution,
        freshness: Freshness,
        prefetcher: MetadataPrefetcher,
        request_builder: RequestBuilder,
        hooks: Hooks,
        decision_logger: BaseDecisionLogger,
        dev_cloner: t.Optional[DevCloner],
    ) -> None:
        self._adapter_ext = adapter_ext
        self._query_cache_client = query_cache_client
        self._run_cache_config = run_cache_config
        self._config = config
        self._manifest = manifest
        self._node_resolution = node_resolution
        self._freshness = freshness
        self._prefetcher = prefetcher
        self._request_builder = request_builder
        self._hooks = hooks
        self._decision_logger = decision_logger
        self._dev_cloner = dev_cloner

        self._total_cache_hits: int = 0
        self._total_time_saved_ms: int = 0
        self._reused_status_warning_emitted: bool = False

        # map of node.unique_id -> CacheBypassedResponse
        # collected in act() and published as untracked executions in record_run_result()
        self.cache_bypass_responses: t.Dict[str, CacheBypassedResponse] = {}

        # unique_ids of nodes cloned at compile time, so a later skip is reported as a clone
        self.dev_cloned_nodes: t.Set[str] = set()

    @property
    def _adapter(self) -> SQLAdapter:
        return self._adapter_ext.adapter

    @property
    def total_cache_hits(self) -> int:
        return self._total_cache_hits

    @property
    def total_time_saved_ms(self) -> int:
        return self._total_time_saved_ms

    def act(
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
        """Act on the server's decision for ``node``.

        Returns:
            - A ``RunResult`` if the node was reused or cloned.
            - A ``NoRunResult`` if the node must be executed normally and confirmed afterwards.
            - ``None`` if the node must be executed normally without confirmation.
        """
        if query_cache_response is None:
            return None

        if isinstance(query_cache_response, CacheBypassedResponse):
            # these get picked up in record_run_result() when the execution completes
            self.cache_bypass_responses[node.unique_id] = query_cache_response
            return None

        self._log_explained_decision(node, query_cache_response)

        if isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
            return self._act_skip(node, query_cache_response)
        if isinstance(query_cache_response, clone_service_models.ReadyToCloneResponse):
            return self._act_clone(node, query_cache_response)
        return self._act_execute(node, query_cache_response)

    @staticmethod
    def _log_explained_decision(
        node: ModelOrSnapshotOrTestOrSeedNode,
        query_cache_response: t.Union[
            sql_service_models.ReadyToExecuteResponse,
            sql_service_models.SkipExecutionResponse,
            clone_service_models.ReadyToCloneResponse,
        ],
    ) -> None:
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

    @staticmethod
    def _act_execute(
        node: ModelOrSnapshotOrTestOrSeedNode,
        response: sql_service_models.ReadyToExecuteResponse,
    ) -> NoRunResult:
        events.fire_debug_event(
            "Received execute response for node {}, request_id: {}",
            node.name,
            response.request_id,
        )
        return NoRunResult(response.request_id, failed_to_clone=False)

    def _act_skip(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        response: sql_service_models.SkipExecutionResponse,
    ) -> RunResult:
        events.fire_debug_event("Received skip execution response for node {}", node.name)
        is_stale = response.explained_decision.is_stale
        self.record_cache_hit(response)
        should_run_hooks = self._run_cache_config.resolve_run_hooks_on_no_op(node.config)
        hooks = self._hooks.handle_pre_hooks(should_run_hooks, node)

        try:
            if node.unique_id in self.dev_cloned_nodes:
                status, message = self.clone_status_and_message(is_stale)
                return RunResult.from_node(node, status, message)
            # SkipExecutionResponse is only produced for models/snapshots/tests,
            # not seeds — narrow the type for resolve_freshness_tolerance.
            status, message = self.no_op_status_and_message(
                is_stale,
                t.cast("t.Union[ModelConfig, SnapshotConfig, TestConfig]", node.config),
            )
            return RunResult.from_node(node, status, message)
        finally:
            # Skips reuse an existing execution.
            self._hooks.track_execution(node, response.execution_id, response)
            self._hooks.handle_post_hooks(
                should_run_hooks,
                node,
                response,
                hooks.context,
                hooks.context_config,
                hooks.hook_ctx,
                response.execution_id,
            )

    def _act_clone(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        response: clone_service_models.ReadyToCloneResponse,
    ) -> t.Union[RunResult, NoRunResult]:
        events.fire_debug_event(
            "Received ready to clone response for node {}, request_id: {}",
            node.name,
            response.request_id,
        )
        is_stale = response.explained_decision.is_stale
        should_run_hooks = True
        hooks = self._hooks.handle_pre_hooks(True, node)

        # Track the confirmed request ID for post-hook metadata updates.
        # This may differ from response.request_id, since a clone creates a new execution.
        confirmed_execution_id: t.Optional[RequestId] = None

        try:
            if response.clone_required_last_modified_epoch is not None:
                current_last_modified_epoch = self._freshness.get_last_modified_epoch(
                    exp.to_table(response.clone_source, dialect=self._node_resolution.dialect)
                )
                if current_last_modified_epoch is None or (
                    current_last_modified_epoch > response.clone_required_last_modified_epoch
                ):
                    events.fire_debug_event(
                        "Unable to clone node '{}' due to table's latest state not matching what is expected. "
                        "Expected last modified epoch: {}, actual last modified epoch: {}.",
                        node.name,
                        response.clone_required_last_modified_epoch,
                        current_last_modified_epoch,
                    )
                    should_run_hooks = False
                    return NoRunResult(response.request_id, failed_to_clone=True)
            existing_relation = self._execute_clone(response)
            self._adapter_ext.commit_if_open()
            if hooks.context is not None:
                self._apply_grants_after_clone(node, hooks.context, existing_relation)
            # when we clone a table, we put it in the relation cache so that the remainder of the
            # invocation knows it exists without hitting the db
            self._adapter_ext.cache_node_relation(node)
            confirmed_execution_id = self.confirm_execution(node, response.request_id)
            self.record_cache_hit(response)
            status, message = self.clone_status_and_message(is_stale)
            return RunResult.from_node(node, status, message)
        except Exception as e:
            self._adapter_ext.rollback()
            should_run_hooks = False
            events.fire_warn_event(
                "Clone failed for node '{}', falling back to full execution: {}",
                node.name,
                str(e),
            )
            return NoRunResult(response.request_id, failed_to_clone=True)
        finally:
            # Clones only have an execution once confirmed.
            self._hooks.handle_post_hooks(
                should_run_hooks,
                node,
                response,
                hooks.context,
                hooks.context_config,
                hooks.hook_ctx,
                confirmed_execution_id,
            )

    def _execute_clone(self, response: clone_service_models.ReadyToCloneResponse) -> t.Any:
        """Clone ``response.clone_source`` into ``response.clone_target``.

        Returns:
            The target relation as it was before the clone, or None if it did not exist.
        """
        with events.downgrade_adapter_error_events():
            # drop the clone target before attempting the clone, otherwise we can run into a problem where we try to clone
            # a table on top of a view
            if (
                existing_relation := self._adapter_ext.fqn_to_cached_relation(response.clone_target)
            ) and existing_relation.type != RelationType.Table:
                self._adapter.drop_relation(existing_relation)

            if self._adapter_ext.IMPLEMENTS_CUSTOM_CLONE:
                self._adapter_ext.clone(
                    response.clone_sqls, response.clone_source, response.clone_target
                )
            else:
                for sql in response.clone_sqls:
                    self._adapter.execute(sql)
        return existing_relation

    def _apply_grants_after_clone(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        context: dict[str, t.Any],
        existing_relation: t.Any,
    ) -> None:
        """Apply the node's configured grants to a freshly cloned target.

        dbt has no Python-level grants step: each materialization (e.g. ``table``, ``clone``) calls
        the ``should_revoke`` and ``apply_grants`` macros itself. A clone bypasses the materialization,
        so the same macros are called here through the node's runtime context, which keeps adapter
        dispatch and any project-level overrides of those macros in effect.

        Args:
            node: The node whose clone target should receive its configured grants.
            context: The node's runtime model context, as used to render hooks.
            existing_relation: The target relation as it was before the clone, or None.
        """
        grant_config = getattr(node.config, "grants", None)
        if not grant_config:
            return
        target_relation = context["this"].incorporate(type="table")
        revoke = context["should_revoke"](existing_relation, full_refresh_mode=True)
        context["apply_grants"](target_relation, grant_config, should_revoke=revoke)
        self._adapter_ext.commit_if_open()

    def run(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        act_result: t.Union[RunResult, NoRunResult, None],
        execute: t.Callable[[], RunResult],
        should_confirm: t.Callable[[RunResult], bool],
    ) -> RunResult:
        """Finish a node's execution given what ``act`` returned for it.

        A ``RunResult`` from ``act`` (a reuse or clone) is returned as is. Otherwise
        ``execute`` runs the node normally and its outcome is recorded: untracked executions
        are published, and a tracked execution (``NoRunResult``) is confirmed when
        ``should_confirm(result)`` holds. In every other case the node's cached target
        metadata is invalidated, because the target was rebuilt without being confirmed.

        Args:
            node: The node being executed.
            act_result: What ``act`` returned for the node.
            execute: Runs the node normally and returns its result.
            should_confirm: Given the execution result, whether to confirm the execution
                with the cache.
        """
        if isinstance(act_result, RunResult):
            return act_result

        execute_start_ts = perf_counter()
        result = execute()

        self.record_run_result(t.cast("ModelOrSnapshotOrSeedNode", node), result)

        if isinstance(act_result, NoRunResult) and should_confirm(result):
            try:
                elapsed_ms = int((perf_counter() - execute_start_ts) * 1000)
                self.confirm_execution(
                    node,
                    act_result.request_id,
                    act_result.failed_to_clone,
                    execution_runtime_ms=elapsed_ms,
                )
            except Exception as e:
                events.fire_warn_event_with_cache_bypass(
                    "execute: request confirmation failed for node {}:\n{}",
                    node.unique_id,
                    str(e),
                )
        else:
            self.invalidate(node)
        return result

    def act_dev_clone(
        self,
        node: ModelOrSnapshotNode,
        clone_response: t.Union[
            clone_service_models.ReadyToCloneResponse, clone_service_models.UnableToCloneResponse
        ],
    ) -> bool:
        """Act on the server's decision to dev clone ``node`` at compile time.

        Returns:
            True if the node was cloned (and is now remembered as dev-cloned), False if the
            server rejected the clone.
        """
        assert self._dev_cloner is not None
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
        self.dev_cloned_nodes.add(node.unique_id)
        return True

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
            self._hooks.track_execution(node, response.execution_id)
            return response.execution_id
        events.fire_debug_event(
            "Execution confirmation failed for node {}, request_id: {}",
            node.unique_id,
            request_id,
        )
        return None

    def record_run_result(self, node: ModelOrSnapshotOrSeedNode, result: RunResult) -> None:
        """Publish the outcome of an execution that ran without a tracked server request."""
        if not (bypass_response := self.cache_bypass_responses.get(node.unique_id)):
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

        self.publish_write_only_execution(bypass_response=bypass_response, outcome=outcome)

    def invalidate(self, node: ModelOrSnapshotOrTestOrSeedNode) -> None:
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
        if node.unique_id in self.cache_bypass_responses:
            # write-only executions refresh the cache in record_run_result() instead
            return

        try:
            self._adapter_ext.clear_cache([self._node_resolution.node_to_table(node)])
        except Exception as e:
            events.fire_debug_event(
                "Failed to clear cached metadata for node {}: {}", node.unique_id, str(e)
            )

    def publish_write_only_execution(
        self,
        bypass_response: CacheBypassedResponse,
        outcome: execution_service_models.ExecutionOutcome,
    ) -> None:
        record = execution_service_models.ExecutionRecord(outcome=outcome)

        original_request = bypass_response.request
        if isinstance(original_request, sql_service_models.SubmitEnrichedSQLRequest):
            if bypass_response.speculative:
                original_request = self.finalize_speculative_request(
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

    def finalize_speculative_request(
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

    def record_cache_hit(
        self,
        response: t.Union[
            sql_service_models.SkipExecutionResponse, clone_service_models.ReadyToCloneResponse
        ],
    ) -> None:
        self._total_cache_hits += 1
        self._total_time_saved_ms += response.execution_runtime_ms or 0

    def cache_hit_run_status(self) -> RunStatus:
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

    def clone_status_and_message(self, is_stale: bool) -> t.Tuple[RunStatus, str]:
        """Return (status, message) for cache-hit clone results.

        When ``emit_reused_status`` is enabled and supported, emit the new status with a
        Fusion-style message describing the clone. Otherwise use the legacy
        ``Success`` + "CLONE" representation.
        """
        status = self.cache_hit_run_status()
        if status is _RUN_STATUS_REUSED:
            suffix = " within tolerance" if is_stale else ""
            return status, "Cloned from other environment" + suffix
        legacy_suffix = " (within tolerance)" if is_stale else ""
        return status, "CLONE" + legacy_suffix

    def no_op_status_and_message(
        self,
        is_stale: bool,
        node_config: t.Union[ModelConfig, SnapshotConfig, TestConfig],
    ) -> t.Tuple[RunStatus, str]:
        """Return (status, message) for cache-hit no-op results.

        When ``emit_reused_status`` is enabled and supported, emit the new status with a
        Fusion-style message describing why the node was reused. Otherwise use
        the legacy ``Success`` + "NO-OP" representation.
        """
        status = self.cache_hit_run_status()
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
