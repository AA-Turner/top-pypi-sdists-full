from __future__ import annotations

import typing as t

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

    def hook_references_target_table(
        self,
        node: ModelOrSnapshotOrTestOrSeedNode,
        rendered_sql: str,
    ) -> bool:
        """Check if a rendered post-hook references the target table.

        Args:
            node: The node being executed
            rendered_sql: The hook SQL after Jinja rendering

        Returns:
            True if the hook references the target table (or this can't be determined),
            False otherwise
        """
        try:
            target_parts = [part.name for part in self._node_resolution.node_to_table(node).parts]
        except Exception as e:
            events.fire_debug_event("Could not resolve target table for post-hooks: {}", str(e))
            return True

        try:
            statements = sqlglot.parse(rendered_sql, dialect=self._node_resolution.dialect)
        except Exception as e:
            events.fire_debug_event("Could not check post-hook for table reference: {}", str(e))
            return True

        for statement in statements:
            if statement is None:
                continue
            for table in statement.find_all(exp.Table):
                normalized = normalize_identifiers(
                    table.copy(), dialect=self._node_resolution.dialect
                )
                reference_parts = [part.name for part in normalized.parts]
                if (
                    reference_parts
                    and len(reference_parts) <= len(target_parts)
                    and reference_parts == target_parts[-len(reference_parts) :]
                ):
                    return True

        return False
