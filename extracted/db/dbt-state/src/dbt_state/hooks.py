from __future__ import annotations

import typing as t
from dataclasses import dataclass

import sqlglot
from dbt.clients.jinja import get_rendered
from dbt.context.providers import generate_runtime_model_context
from dbt.contracts.graph.nodes import GenericTestNode, ModelNode, SingularTestNode, SnapshotNode
from query_cache_common.models import shared_models
from query_cache_common.models.services import (
    clone_service_models,
    execution_service_models,
    sql_service_models,
)
from sqlglot import exp
from sqlglot.optimizer.normalize_identifiers import normalize_identifiers

from dbt_state import events
from dbt_state.adapters import BaseAdapterExtension
from dbt_state.config import RunCacheConfig
from dbt_state.freshness import Freshness
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.node_resolution import NodeResolution

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

if t.TYPE_CHECKING:
    from dbt_state._typing import ModelOrSnapshotOrTestNode, ModelOrSnapshotOrTestOrSeedNode

RequestId = str


class PreHookResult(t.NamedTuple):
    """Rendering context and adapter hook state produced by running pre-hooks."""

    context: t.Optional[dict[str, t.Any]] = None
    context_config: t.Any = None
    hook_ctx: t.Any = None


@dataclass
class TrackedExecution:
    unique_id: str
    node: ModelOrSnapshotOrTestOrSeedNode
    execution_id: RequestId
    skip_update: bool
    warn_on_skip: bool


class Hooks:
    """Runs dbt pre- and post-hooks around reused (skipped or cloned) nodes.

    Also refreshes the stored last-modified metadata after post-hooks modify the target table,
    and commits through the adapter extension after post-hooks.
    """

    def __init__(
        self,
        adapter_ext: BaseAdapterExtension,
        node_resolution: NodeResolution,
        freshness: Freshness,
        query_cache_client: QueryCacheGrpcClient,
        run_cache_config: RunCacheConfig,
        node_execution_type: t.Callable[[ModelOrSnapshotOrTestNode], str],
        config: t.Any,
        manifest: t.Any,
    ) -> None:
        self._adapter_ext = adapter_ext
        self._node_resolution = node_resolution
        self._freshness = freshness
        self._query_cache_client = query_cache_client
        self._run_cache_config = run_cache_config
        self._node_execution_type = node_execution_type
        self._config = config
        self._manifest = manifest

        # Executions confirmed or reused during this run, kept so that tables modified by
        # on-run-end hooks can have their stored last_modified refreshed.
        # unique_id -> (node, execution_id, skip_update, warn_on_skip)
        self._tracked_executions: t.Dict[str, TrackedExecution] = {}
        self._on_run_end_baseline: t.Dict[str, t.Optional[int]] = {}
        self._on_run_end_succeeded: t.Set[str] = set()
        self._on_run_end_targets: t.List[t.Tuple[t.List[str], str]] = []

    def handle_pre_hooks(
        self,
        should_run_hooks: bool,
        node: ModelOrSnapshotOrTestOrSeedNode,
    ) -> PreHookResult:
        """Run the adapter pre-model hook and the node's pre-hooks when hooks should run.

        Returns the rendering context, its config and the adapter hook context, which the
        caller passes on to `handle_post_hooks`. All fields are None when hooks are not run.
        """
        if not should_run_hooks:
            return PreHookResult()

        context = generate_runtime_model_context(node, self._config, self._manifest)
        context_config = context["config"]
        hook_ctx = self._adapter_ext.adapter.pre_model_hook(context_config)
        for hook in getattr(node.config, "pre_hook", []):
            self.execute_hook(hook, get_rendered(hook.sql, context))
        return PreHookResult(context, context_config, hook_ctx)

    def handle_post_hooks(
        self,
        should_run_hooks: bool,
        node: ModelOrSnapshotOrTestOrSeedNode,
        query_cache_response: t.Union[
            sql_service_models.SkipExecutionResponse,
            clone_service_models.ReadyToCloneResponse,
            None,
        ],
        context: dict[str, t.Any],
        context_config: t.Any,
        hook_ctx: t.Any,
        execution_id: t.Optional[RequestId],
    ) -> None:
        if should_run_hooks:
            pre_hook_last_modified = None
            post_hooks = getattr(node.config, "post_hook", [])

            if post_hooks:
                try:
                    _, pre_hook_last_modified = (
                        self._freshness.get_target_table_type_and_last_modified_epoch(node)
                    )
                except Exception:
                    events.fire_debug_event(
                        "Skipping post-hook handle for node {} due to failure when fetching last modified epoch",
                        node.unique_id,
                    )

            # Hooks are rendered and executed one at a time, so a hook's rendering sees the
            # effects of the hooks before it. Each hook is rendered exactly once, and the
            # rendered SQL is kept to check for target table references afterwards.
            rendered_sqls = []
            for hook in post_hooks:
                rendered_sql = get_rendered(hook.sql, context)
                rendered_sqls.append(rendered_sql)
                self.execute_hook(hook, rendered_sql)

            references_target_table = any(
                self.hook_references_target_table(node, rendered_sql)
                for rendered_sql in rendered_sqls
            )

            self._adapter_ext.commit_if_open()
            self._adapter_ext.adapter.post_model_hook(context_config, hook_ctx)

            if (
                references_target_table
                and pre_hook_last_modified
                and execution_id is not None
                and isinstance(
                    query_cache_response,
                    (
                        sql_service_models.SkipExecutionResponse,
                        clone_service_models.ReadyToCloneResponse,
                    ),
                )
            ):
                skip_update, warn_on_skip = self.resolve_no_op_post_hook_policy(
                    node, query_cache_response
                )
                self.update_metadata_after_post_hooks(
                    node,
                    execution_id,
                    pre_hook_last_modified,
                    skip_update,
                    warn_on_skip,
                )

    def resolve_no_op_post_hook_policy(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        query_cache_response: t.Union[
            sql_service_models.SkipExecutionResponse,
            clone_service_models.ReadyToCloneResponse,
        ],
    ) -> t.Tuple[bool, bool]:
        """Decide how to treat the post-hook timestamp update after a NO-OP.

        Returns:
            (skip_update, warn_on_skip). skip_update is set for NO-OPs under lag tolerance,
            where bumping the stored last_modified_epoch would reset the output's age and
            keep a stale result eligible for reuse. warn_on_skip is set when the server will
            also rebuild the model on the next run, which it only does for VIEW/FULL when
            external modifications are not ignored.
        """
        if not isinstance(query_cache_response, sql_service_models.SkipExecutionResponse):
            return False, False

        if not isinstance(node, (ModelNode, SnapshotNode, GenericTestNode, SingularTestNode)):
            return False, False

        if not isinstance(node.config, (ModelConfig, SnapshotConfig, TestConfig)):
            return False, False

        skip_update = self._run_cache_config.resolve_freshness_tolerance(node.config) > 0
        warn_on_skip = (
            skip_update
            and not self._run_cache_config.resolve_ignore_external_modifications(node.config)
            and shared_models.ModelExecutionType(self._node_execution_type(node))
            in (shared_models.ModelExecutionType.VIEW, shared_models.ModelExecutionType.FULL)
        )
        return skip_update, warn_on_skip

    def execute_hook(self, hook: t.Any, rendered_sql: str) -> None:
        if rendered_sql.strip():
            self._adapter_ext.adapter.execute(rendered_sql, auto_begin=hook.transaction)

    def update_metadata_after_post_hooks(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        execution_id: RequestId,
        pre_hook_last_modified: t.Optional[int],
        skip_update: bool = False,
        warn_on_skip: bool = False,
    ) -> None:
        """Update metadata after post-hooks complete. Best-effort.

        Args:
            node: The node whose post-hooks just executed
            execution_id: Execution ID from the original confirmation
            pre_hook_last_modified: Target table timestamp before post-hooks
            skip_update: Do not store the post-hook timestamp. Set for NO-OPs under lag
                tolerance, where bumping the stored last_modified_epoch would reset the
                output's age and keep a stale result eligible for reuse indefinitely
            warn_on_skip: Warn when the update is skipped because the post-hooks modified
                the target table, as the next run will then rebuild the model
        """
        try:
            _, post_hook_last_modified = (
                self._freshness.get_target_table_type_and_last_modified_epoch(node)
            )

            if post_hook_last_modified is None or post_hook_last_modified == pre_hook_last_modified:
                return

            if skip_update:
                if warn_on_skip:
                    events.fire_warn_event(
                        "Post-hook for '{}' modified the target table after a NO-OP. The stored "
                        "last_modified timestamp was not updated so that it does not extend the "
                        "lag_tolerance window; as a result, this model will be rebuilt on the next "
                        "run. To avoid this, disable execute_hooks_on_any_reuse or remove post-hook "
                        "statements that modify the target table.",
                        node.unique_id,
                    )
                return

            update_request = execution_service_models.UpdateExecutionMetadataRequest(
                execution_id=execution_id,
                last_modified_epoch=post_hook_last_modified,
            )

            self._query_cache_client.update_execution_metadata(update_request)

        except Exception as e:
            events.fire_warn_event(
                "Failed to update post-hook metadata for '{}': {}", node.unique_id, str(e)
            )

    def track_execution(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        execution_id: RequestId,
        query_cache_response: t.Union[
            sql_service_models.SkipExecutionResponse,
            clone_service_models.ReadyToCloneResponse,
            None,
        ] = None,
    ) -> None:
        """Remember an execution confirmed or reused this run, for on-run-end refresh."""
        skip_update, warn_on_skip = (
            self.resolve_no_op_post_hook_policy(node, query_cache_response)
            if query_cache_response is not None
            else (False, False)
        )
        self._tracked_executions[node.unique_id] = TrackedExecution(
            node.unique_id, node, execution_id, skip_update, warn_on_skip
        )

    def begin_on_run_end(self) -> None:
        """Start tracking on-run-end hooks: reset state and resolve tracked target tables."""
        self._on_run_end_baseline = {}
        self._on_run_end_succeeded = set()
        self._on_run_end_targets = []
        for tracked_execution in self._tracked_executions.values():
            try:
                parts = [
                    part.name
                    for part in self._node_resolution.node_to_table(tracked_execution.node).parts
                ]
            except Exception as e:
                events.fire_debug_event(
                    "Could not resolve target table for '{}' on-run-end: {}",
                    tracked_execution.unique_id,
                    str(e),
                )
                continue
            if parts:
                self._on_run_end_targets.append((parts, tracked_execution.unique_id))
        self._baseline_on_run_end_targets()

    def _baseline_on_run_end_targets(self) -> None:
        unique_ids = [uid for _, uid in self._on_run_end_targets]
        if not unique_ids:
            return
        if self._freshness.uses_heuristic_clock_for_last_modified:
            epoch = self._freshness.get_heuristic_now_epoch()
            self._on_run_end_baseline = {uid: epoch for uid in unique_ids}
            return
        nodes = [self._tracked_executions[uid].node for uid in unique_ids]
        epochs = self._freshness.get_target_actual_last_modified_epochs(nodes)
        self._on_run_end_baseline = {uid: epochs.get(uid) for uid in unique_ids}

    def _match_tracked_node(self, parts: t.List[str]) -> t.Optional[str]:
        """Return the unique_id of the single tracked table `parts` names, else None."""
        matches = {
            unique_id
            for target_parts, unique_id in self._on_run_end_targets
            if self._parts_match(parts, target_parts)
        }
        return next(iter(matches)) if len(matches) == 1 else None

    def _matched_unique_ids(self, sql: str) -> t.Set[str]:
        refs = self._referenced_table_parts(sql) or []
        matched = (self._match_tracked_node(parts) for parts in refs)
        return {uid for uid in matched if uid is not None}

    def before_on_run_end_statement(self, sql: str) -> t.Set[str]:
        """Return the unique_ids of the tracked tables a statement writes. Best-effort."""
        return self._matched_unique_ids(sql)

    def after_on_run_end_statement(self, unique_ids: t.Iterable[str]) -> None:
        """Mark tracked tables as written by a successfully executed on-run-end statement."""
        self._on_run_end_succeeded.update(unique_ids)

    def update_metadata_after_on_run_end(self) -> None:
        """Refresh stored last_modified for tables modified by on-run-end hooks. Best-effort.

        Without this, the next run sees the on-run-end modification as an external
        modification and rebuilds the model.
        """
        try:
            afters = self._freshness.get_target_actual_last_modified_epochs(
                [
                    self._tracked_executions[uid].node
                    for uid in self._on_run_end_baseline
                    if uid in self._on_run_end_succeeded
                ]
            )
        except Exception as e:
            events.fire_warn_event("Failed to read on-run-end last modified timestamps: {}", str(e))
            afters = {}
        for unique_id, before in self._on_run_end_baseline.items():
            if unique_id not in self._on_run_end_succeeded:
                continue
            tracked_execution = self._tracked_executions[unique_id]
            try:
                after = afters.get(unique_id)
                if after is None or before is None or after <= before:
                    continue
                if tracked_execution.skip_update:
                    if tracked_execution.warn_on_skip:
                        events.fire_warn_event(
                            "on-run-end hooks modified '{}' after a NO-OP. The stored "
                            "last_modified timestamp was not updated so that it does not extend "
                            "the lag_tolerance window; as a result, this model will be rebuilt on "
                            "the next run.",
                            unique_id,
                        )
                    continue
                self._query_cache_client.update_execution_metadata(
                    execution_service_models.UpdateExecutionMetadataRequest(
                        execution_id=tracked_execution.execution_id, last_modified_epoch=after
                    )
                )
            except Exception as e:
                events.fire_warn_event(
                    "Failed to update on-run-end metadata for '{}': {}", unique_id, str(e)
                )
        self._on_run_end_baseline = {}
        self._on_run_end_succeeded = set()

    def _referenced_table_parts(self, rendered_sql: str) -> t.Optional[t.List[t.List[str]]]:
        """Parse hook SQL once and return the normalized table references.

        Args:
            rendered_sql: The hook SQL after Jinja rendering

        Returns None if the SQL can't be parsed.
        """
        dialect = self._node_resolution.dialect
        try:
            statements = sqlglot.parse(rendered_sql, dialect=dialect)
        except Exception as e:
            events.fire_debug_event("Could not check hook for table reference: {}", str(e))
            return None

        refs: t.List[t.List[str]] = []
        for statement in statements:
            if statement is None:
                continue
            for table in statement.find_all(exp.Table):
                normalized = normalize_identifiers(table.copy(), dialect=dialect)
                parts = [part.name for part in normalized.parts]
                if parts:
                    refs.append(parts)
        return refs

    def _refs_match_node(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        refs: t.List[t.List[str]],
        default_if_unresolved: bool = True,
    ) -> bool:
        """Check if any table reference is a suffix of the node's target table.

        Returns `default_if_unresolved` if the target table can't be resolved.
        """
        try:
            target_parts = [part.name for part in self._node_resolution.node_to_table(node).parts]
        except Exception as e:
            events.fire_debug_event("Could not resolve target table for hooks: {}", str(e))
            return default_if_unresolved

        return any(self._parts_match(parts, target_parts) for parts in refs)

    @staticmethod
    def _parts_match(parts: t.List[str], target_parts: t.List[str]) -> bool:
        """Check if `parts` is a suffix of the resolved `target_parts`."""
        return len(parts) <= len(target_parts) and parts == target_parts[-len(parts) :]

    def hook_references_target_table(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        rendered_sql: str,
    ) -> bool:
        """Check if a rendered hook references the target table.

        Args:
            node: The node being executed
            rendered_sql: The hook SQL after Jinja rendering

        Returns:
            True if the hook references the target table, False otherwise
        """
        if not rendered_sql.strip():
            # Rendering may have executed writes itself (run_query, statement blocks)
            return True
        refs = self._referenced_table_parts(rendered_sql)
        if refs is None:
            return True
        return self._refs_match_node(node, refs)
